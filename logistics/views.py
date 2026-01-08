"""
Views for Logistics & Supply Chain Management Module
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta
from .models import (
    Warehouse, Inventory, Shipment, ShipmentItem,
    Route, Delivery, StockMovement
)
from .forms import (
    WarehouseForm, InventoryForm, ShipmentForm, ShipmentItemForm,
    RouteForm, DeliveryForm, StockMovementForm
)


# Dashboard Views
def logistics_dashboard(request):
    """Main logistics dashboard"""
    # Get key metrics
    total_warehouses = Warehouse.objects.filter(is_active=True).count()
    total_inventory_value = Inventory.objects.aggregate(
        total=Sum('total_value')
    )['total'] or 0
    
    active_shipments = Shipment.objects.filter(
        status__in=['pending', 'preparing', 'in_transit']
    ).count()
    
    pending_deliveries = Delivery.objects.filter(
        status__in=['scheduled', 'in_progress']
    ).count()
    
    # Low stock items
    low_stock_items = Inventory.objects.filter(
        quantity_available__lt=F('reorder_level')
    ).count()
    
    # Recent shipments
    recent_shipments = Shipment.objects.select_related(
        'origin_warehouse', 'destination_warehouse'
    ).order_by('-created_at')[:5]
    
    # Shipments by status
    shipment_stats = Shipment.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Warehouse utilization
    warehouses = Warehouse.objects.filter(is_active=True)
    for warehouse in warehouses:
        warehouse.utilization_percentage = warehouse.get_utilization_percentage()
    
    context = {
        'total_warehouses': total_warehouses,
        'total_inventory_value': total_inventory_value,
        'active_shipments': active_shipments,
        'pending_deliveries': pending_deliveries,
        'low_stock_items': low_stock_items,
        'recent_shipments': recent_shipments,
        'shipment_stats': shipment_stats,
        'warehouses': warehouses,
    }
    
    return render(request, 'logistics/dashboard.html', context)


# Warehouse Views
def warehouse_list(request):
    """List all warehouses"""
    search_query = request.GET.get('search', '')
    warehouse_type = request.GET.get('type', '')
    
    warehouses = Warehouse.objects.all()
    
    if search_query:
        warehouses = warehouses.filter(
            Q(code__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    if warehouse_type:
        warehouses = warehouses.filter(warehouse_type=warehouse_type)
    
    # Calculate utilization for each warehouse
    for warehouse in warehouses:
        warehouse.utilization_percentage = warehouse.get_utilization_percentage()
    
    context = {
        'warehouses': warehouses,
        'search_query': search_query,
        'warehouse_type': warehouse_type,
    }
    
    return render(request, 'logistics/warehouse_list.html', context)


def warehouse_detail(request, pk):
    """View warehouse details"""
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    # Get inventory for this warehouse
    inventory_items = Inventory.objects.filter(warehouse=warehouse)
    total_items = inventory_items.count()
    total_value = inventory_items.aggregate(Sum('total_value'))['total_value__sum'] or 0
    
    # Get recent stock movements
    recent_movements = StockMovement.objects.filter(
        Q(inventory__warehouse=warehouse) |
        Q(from_warehouse=warehouse) |
        Q(to_warehouse=warehouse)
    ).order_by('-movement_date')[:10]
    
    # Get shipments
    outbound_shipments = Shipment.objects.filter(
        origin_warehouse=warehouse
    ).order_by('-created_at')[:5]
    
    inbound_shipments = Shipment.objects.filter(
        destination_warehouse=warehouse
    ).order_by('-created_at')[:5]
    
    context = {
        'warehouse': warehouse,
        'utilization_percentage': warehouse.get_utilization_percentage(),
        'total_items': total_items,
        'total_value': total_value,
        'inventory_items': inventory_items[:10],
        'recent_movements': recent_movements,
        'outbound_shipments': outbound_shipments,
        'inbound_shipments': inbound_shipments,
    }
    
    return render(request, 'logistics/warehouse_detail.html', context)


def warehouse_create(request):
    """Create a new warehouse"""
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, f'Warehouse {warehouse.code} created successfully!')
            return redirect('logistics:warehouse_detail', pk=warehouse.pk)
    else:
        form = WarehouseForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'logistics/warehouse_form.html', context)


def warehouse_update(request, pk):
    """Update warehouse details"""
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            warehouse = form.save()
            messages.success(request, f'Warehouse {warehouse.code} updated successfully!')
            return redirect('logistics:warehouse_detail', pk=warehouse.pk)
    else:
        form = WarehouseForm(instance=warehouse)
    
    context = {'form': form, 'warehouse': warehouse, 'action': 'Update'}
    return render(request, 'logistics/warehouse_form.html', context)


def warehouse_delete(request, pk):
    """Delete a warehouse"""
    warehouse = get_object_or_404(Warehouse, pk=pk)
    
    if request.method == 'POST':
        warehouse_code = warehouse.code
        warehouse.delete()
        messages.success(request, f'Warehouse {warehouse_code} deleted successfully!')
        return redirect('logistics:warehouse_list')
    
    context = {'warehouse': warehouse}
    return render(request, 'logistics/warehouse_confirm_delete.html', context)


# Inventory Views
def inventory_list(request):
    """List all inventory items"""
    search_query = request.GET.get('search', '')
    warehouse_id = request.GET.get('warehouse', '')
    low_stock = request.GET.get('low_stock', '')
    
    inventory_items = Inventory.objects.select_related('warehouse').all()
    
    if search_query:
        inventory_items = inventory_items.filter(
            Q(product_code__icontains=search_query) |
            Q(product_name__icontains=search_query)
        )
    
    if warehouse_id:
        inventory_items = inventory_items.filter(warehouse_id=warehouse_id)
    
    if low_stock:
        inventory_items = inventory_items.filter(
            quantity_available__lt=F('reorder_level')
        )
    
    # Get warehouses for filter
    warehouses = Warehouse.objects.filter(is_active=True)
    
    # Calculate totals
    total_value = inventory_items.aggregate(Sum('total_value'))['total_value__sum'] or 0
    total_quantity = inventory_items.aggregate(Sum('quantity_on_hand'))['quantity_on_hand__sum'] or 0
    
    context = {
        'inventory_items': inventory_items,
        'warehouses': warehouses,
        'search_query': search_query,
        'selected_warehouse': warehouse_id,
        'low_stock_filter': low_stock,
        'total_value': total_value,
        'total_quantity': total_quantity,
    }
    
    return render(request, 'logistics/inventory_list.html', context)


def inventory_detail(request, pk):
    """View inventory item details"""
    inventory = get_object_or_404(Inventory.objects.select_related('warehouse'), pk=pk)
    
    # Get stock movements for this inventory
    stock_movements = StockMovement.objects.filter(
        inventory=inventory
    ).order_by('-movement_date')[:20]
    
    context = {
        'inventory': inventory,
        'stock_movements': stock_movements,
        'is_below_reorder': inventory.is_below_reorder_level(),
    }
    
    return render(request, 'logistics/inventory_detail.html', context)


def inventory_create(request):
    """Create a new inventory item"""
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.update_totals()
            inventory.save()
            messages.success(request, f'Inventory item {inventory.product_code} created successfully!')
            return redirect('logistics:inventory_detail', pk=inventory.pk)
    else:
        form = InventoryForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'logistics/inventory_form.html', context)


def inventory_update(request, pk):
    """Update inventory item"""
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.update_totals()
            inventory.save()
            messages.success(request, f'Inventory item {inventory.product_code} updated successfully!')
            return redirect('logistics:inventory_detail', pk=inventory.pk)
    else:
        form = InventoryForm(instance=inventory)
    
    context = {'form': form, 'inventory': inventory, 'action': 'Update'}
    return render(request, 'logistics/inventory_form.html', context)


def inventory_delete(request, pk):
    """Delete an inventory item"""
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        product_code = inventory.product_code
        inventory.delete()
        messages.success(request, f'Inventory item {product_code} deleted successfully!')
        return redirect('logistics:inventory_list')
    
    context = {'inventory': inventory}
    return render(request, 'logistics/inventory_confirm_delete.html', context)


# Shipment Views
def shipment_list(request):
    """List all shipments"""
    search_query = request.GET.get('search', '')
    status = request.GET.get('status', '')
    shipment_type = request.GET.get('type', '')
    
    shipments = Shipment.objects.select_related(
        'origin_warehouse', 'destination_warehouse'
    ).all()
    
    if search_query:
        shipments = shipments.filter(
            Q(shipment_number__icontains=search_query) |
            Q(carrier_name__icontains=search_query) |
            Q(tracking_number__icontains=search_query)
        )
    
    if status:
        shipments = shipments.filter(status=status)
    
    if shipment_type:
        shipments = shipments.filter(shipment_type=shipment_type)
    
    shipments = shipments.order_by('-created_at')
    
    context = {
        'shipments': shipments,
        'search_query': search_query,
        'status_filter': status,
        'type_filter': shipment_type,
    }
    
    return render(request, 'logistics/shipment_list.html', context)


def shipment_detail(request, pk):
    """View shipment details"""
    shipment = get_object_or_404(
        Shipment.objects.select_related('origin_warehouse', 'destination_warehouse'),
        pk=pk
    )
    
    # Get shipment items
    items = ShipmentItem.objects.filter(shipment=shipment)
    
    # Calculate totals
    total_quantity = items.aggregate(Sum('quantity_shipped'))['quantity_shipped__sum'] or 0
    total_weight = items.aggregate(Sum('weight'))['weight__sum'] or 0
    total_packages = items.aggregate(Sum('package_count'))['package_count__sum'] or 0
    
    context = {
        'shipment': shipment,
        'items': items,
        'total_quantity': total_quantity,
        'total_weight': total_weight,
        'total_packages': total_packages,
        'is_delayed': shipment.is_delayed(),
    }
    
    return render(request, 'logistics/shipment_detail.html', context)


def shipment_create(request):
    """Create a new shipment"""
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            shipment = form.save()
            messages.success(request, f'Shipment {shipment.shipment_number} created successfully!')
            return redirect('logistics:shipment_detail', pk=shipment.pk)
    else:
        form = ShipmentForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'logistics/shipment_form.html', context)


def shipment_update(request, pk):
    """Update shipment"""
    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        form = ShipmentForm(request.POST, instance=shipment)
        if form.is_valid():
            shipment = form.save()
            messages.success(request, f'Shipment {shipment.shipment_number} updated successfully!')
            return redirect('logistics:shipment_detail', pk=shipment.pk)
    else:
        form = ShipmentForm(instance=shipment)
    
    context = {'form': form, 'shipment': shipment, 'action': 'Update'}
    return render(request, 'logistics/shipment_form.html', context)


def shipment_delete(request, pk):
    """Delete a shipment"""
    shipment = get_object_or_404(Shipment, pk=pk)
    
    if request.method == 'POST':
        shipment_number = shipment.shipment_number
        shipment.delete()
        messages.success(request, f'Shipment {shipment_number} deleted successfully!')
        return redirect('logistics:shipment_list')
    
    context = {'shipment': shipment}
    return render(request, 'logistics/shipment_confirm_delete.html', context)


# Route Views
def route_list(request):
    """List all routes"""
    search_query = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    routes = Route.objects.select_related('start_warehouse').all()
    
    if search_query:
        routes = routes.filter(
            Q(route_code__icontains=search_query) |
            Q(route_name__icontains=search_query)
        )
    
    if status:
        routes = routes.filter(status=status)
    
    context = {
        'routes': routes,
        'search_query': search_query,
        'status_filter': status,
    }
    
    return render(request, 'logistics/route_list.html', context)


def route_detail(request, pk):
    """View route details"""
    route = get_object_or_404(Route.objects.select_related('start_warehouse'), pk=pk)
    
    # Get deliveries using this route
    deliveries = Delivery.objects.filter(route=route).order_by('-scheduled_date')[:10]
    
    context = {
        'route': route,
        'deliveries': deliveries,
    }
    
    return render(request, 'logistics/route_detail.html', context)


def route_create(request):
    """Create a new route"""
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            route = form.save()
            messages.success(request, f'Route {route.route_code} created successfully!')
            return redirect('logistics:route_detail', pk=route.pk)
    else:
        form = RouteForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'logistics/route_form.html', context)


def route_update(request, pk):
    """Update route"""
    route = get_object_or_404(Route, pk=pk)
    
    if request.method == 'POST':
        form = RouteForm(request.POST, instance=route)
        if form.is_valid():
            route = form.save()
            messages.success(request, f'Route {route.route_code} updated successfully!')
            return redirect('logistics:route_detail', pk=route.pk)
    else:
        form = RouteForm(instance=route)
    
    context = {'form': form, 'route': route, 'action': 'Update'}
    return render(request, 'logistics/route_form.html', context)


def route_delete(request, pk):
    """Delete a route"""
    route = get_object_or_404(Route, pk=pk)
    
    if request.method == 'POST':
        route_code = route.route_code
        route.delete()
        messages.success(request, f'Route {route_code} deleted successfully!')
        return redirect('logistics:route_list')
    
    context = {'route': route}
    return render(request, 'logistics/route_confirm_delete.html', context)


# Delivery Views
def delivery_list(request):
    """List all deliveries"""
    search_query = request.GET.get('search', '')
    status = request.GET.get('status', '')
    
    deliveries = Delivery.objects.select_related('route', 'shipment').all()
    
    if search_query:
        deliveries = deliveries.filter(
            Q(delivery_number__icontains=search_query) |
            Q(delivery_contact__icontains=search_query)
        )
    
    if status:
        deliveries = deliveries.filter(status=status)
    
    deliveries = deliveries.order_by('-scheduled_date')
    
    context = {
        'deliveries': deliveries,
        'search_query': search_query,
        'status_filter': status,
    }
    
    return render(request, 'logistics/delivery_list.html', context)


def delivery_detail(request, pk):
    """View delivery details"""
    delivery = get_object_or_404(
        Delivery.objects.select_related('route', 'shipment'),
        pk=pk
    )
    
    context = {
        'delivery': delivery,
        'is_overdue': delivery.is_overdue(),
    }
    
    return render(request, 'logistics/delivery_detail.html', context)


def delivery_create(request):
    """Create a new delivery"""
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            delivery = form.save()
            messages.success(request, f'Delivery {delivery.delivery_number} created successfully!')
            return redirect('logistics:delivery_detail', pk=delivery.pk)
    else:
        form = DeliveryForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'logistics/delivery_form.html', context)


def delivery_update(request, pk):
    """Update delivery"""
    delivery = get_object_or_404(Delivery, pk=pk)
    
    if request.method == 'POST':
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            delivery = form.save()
            messages.success(request, f'Delivery {delivery.delivery_number} updated successfully!')
            return redirect('logistics:delivery_detail', pk=delivery.pk)
    else:
        form = DeliveryForm(instance=delivery)
    
    context = {'form': form, 'delivery': delivery, 'action': 'Update'}
    return render(request, 'logistics/delivery_form.html', context)


def delivery_delete(request, pk):
    """Delete a delivery"""
    delivery = get_object_or_404(Delivery, pk=pk)
    
    if request.method == 'POST':
        delivery_number = delivery.delivery_number
        delivery.delete()
        messages.success(request, f'Delivery {delivery_number} deleted successfully!')
        return redirect('logistics:delivery_list')
    
    context = {'delivery': delivery}
    return render(request, 'logistics/delivery_confirm_delete.html', context)


# Stock Movement Views
def stock_movement_list(request):
    """List all stock movements"""
    search_query = request.GET.get('search', '')
    movement_type = request.GET.get('type', '')
    
    movements = StockMovement.objects.select_related(
        'inventory', 'inventory__warehouse', 'shipment'
    ).all()
    
    if search_query:
        movements = movements.filter(
            Q(movement_number__icontains=search_query) |
            Q(reference_document__icontains=search_query)
        )
    
    if movement_type:
        movements = movements.filter(movement_type=movement_type)
    
    movements = movements.order_by('-movement_date')
    
    context = {
        'movements': movements,
        'search_query': search_query,
        'type_filter': movement_type,
    }
    
    return render(request, 'logistics/stock_movement_list.html', context)


def stock_movement_detail(request, pk):
    """View stock movement details"""
    movement = get_object_or_404(
        StockMovement.objects.select_related(
            'inventory', 'inventory__warehouse', 'shipment',
            'from_warehouse', 'to_warehouse'
        ),
        pk=pk
    )
    
    context = {'movement': movement}
    return render(request, 'logistics/stock_movement_detail.html', context)


def stock_movement_create(request):
    """Create a new stock movement"""
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.calculate_total()
            movement.save()
            messages.success(request, f'Stock movement {movement.movement_number} created successfully!')
            return redirect('logistics:stock_movement_detail', pk=movement.pk)
    else:
        form = StockMovementForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'logistics/stock_movement_form.html', context)
