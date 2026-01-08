"""
Maintenance & Asset Management Views
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Asset, AssetCategory, PreventiveMaintenance, WorkOrder, MaintenanceLog
from .forms import (
    AssetForm, AssetCategoryForm, PreventiveMaintenanceForm,
    WorkOrderForm, MaintenanceLogForm
)


# ==================== Dashboard ====================

@login_required
def maintenance_dashboard(request):
    """Maintenance & Asset Management Dashboard"""
    
    # Date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    
    # Asset Statistics
    total_assets = Asset.objects.count()
    operational_assets = Asset.objects.filter(status='operational').count()
    maintenance_assets = Asset.objects.filter(status='maintenance').count()
    repair_assets = Asset.objects.filter(status='repair').count()
    
    # Assets by condition
    excellent_condition = Asset.objects.filter(condition='excellent').count()
    poor_condition = Asset.objects.filter(condition='poor').count()
    critical_condition = Asset.objects.filter(condition='critical').count()
    
    # Preventive Maintenance Statistics
    total_pm = PreventiveMaintenance.objects.filter(status='active').count()
    overdue_pm = PreventiveMaintenance.objects.filter(
        status='active',
        next_due_date__lt=today
    ).count()
    due_soon_pm = PreventiveMaintenance.objects.filter(
        status='active',
        next_due_date__gte=today,
        next_due_date__lte=today + timedelta(days=7)
    ).count()
    
    # Work Order Statistics
    total_wo = WorkOrder.objects.count()
    open_wo = WorkOrder.objects.filter(
        status__in=['submitted', 'approved', 'assigned', 'in_progress']
    ).count()
    overdue_wo = WorkOrder.objects.filter(
        status__in=['submitted', 'approved', 'assigned', 'in_progress'],
        scheduled_end__lt=timezone.now()
    ).count()
    
    # Recent Work Orders
    recent_work_orders = WorkOrder.objects.select_related(
        'asset', 'assigned_to'
    ).all()[:5]
    
    # Upcoming PM
    upcoming_pm = PreventiveMaintenance.objects.filter(
        status='active',
        next_due_date__gte=today
    ).select_related('asset').order_by('next_due_date')[:5]
    
    # Assets requiring maintenance
    assets_maintenance_due = Asset.objects.filter(
        next_maintenance_date__lte=today
    )[:5]
    
    # Recent Maintenance Logs
    recent_logs = MaintenanceLog.objects.select_related(
        'asset', 'technician'
    ).all()[:5]
    
    # Calculate availability
    if total_assets > 0:
        availability_rate = (operational_assets / total_assets) * 100
    else:
        availability_rate = 0
    
    context = {
        'total_assets': total_assets,
        'operational_assets': operational_assets,
        'maintenance_assets': maintenance_assets,
        'repair_assets': repair_assets,
        'availability_rate': availability_rate,
        
        'excellent_condition': excellent_condition,
        'poor_condition': poor_condition,
        'critical_condition': critical_condition,
        
        'total_pm': total_pm,
        'overdue_pm': overdue_pm,
        'due_soon_pm': due_soon_pm,
        
        'total_wo': total_wo,
        'open_wo': open_wo,
        'overdue_wo': overdue_wo,
        
        'recent_work_orders': recent_work_orders,
        'upcoming_pm': upcoming_pm,
        'assets_maintenance_due': assets_maintenance_due,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'maintenance/dashboard.html', context)


# ==================== Asset Views ====================

@login_required
def asset_list(request):
    """List all assets"""
    assets = Asset.objects.select_related('category', 'assigned_to').all()
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        assets = assets.filter(status=status_filter)
    
    condition_filter = request.GET.get('condition')
    if condition_filter:
        assets = assets.filter(condition=condition_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        assets = assets.filter(
            Q(asset_number__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(serial_number__icontains=search_query)
        )
    
    context = {
        'assets': assets,
        'status_filter': status_filter,
        'condition_filter': condition_filter,
        'search_query': search_query,
    }
    return render(request, 'maintenance/asset_list.html', context)


@login_required
def asset_detail(request, pk):
    """View asset details"""
    asset = get_object_or_404(
        Asset.objects.select_related('category', 'assigned_to', 'created_by'),
        pk=pk
    )
    
    # Get related records
    work_orders = asset.work_orders.all()[:10]
    maintenance_logs = asset.maintenance_logs.all()[:10]
    preventive_maintenances = asset.preventive_maintenances.all()
    
    context = {
        'asset': asset,
        'work_orders': work_orders,
        'maintenance_logs': maintenance_logs,
        'preventive_maintenances': preventive_maintenances,
    }
    return render(request, 'maintenance/asset_detail.html', context)


@login_required
def asset_create(request):
    """Create new asset"""
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.created_by = request.user
            asset.save()
            messages.success(request, f'Asset {asset.asset_number} created successfully!')
            return redirect('maintenance:asset_detail', pk=asset.pk)
    else:
        form = AssetForm()
    
    context = {'form': form}
    return render(request, 'maintenance/asset_form.html', context)


@login_required
def asset_update(request, pk):
    """Update asset"""
    asset = get_object_or_404(Asset, pk=pk)
    
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated successfully!')
            return redirect('maintenance:asset_detail', pk=asset.pk)
    else:
        form = AssetForm(instance=asset)
    
    context = {
        'form': form,
        'asset': asset,
    }
    return render(request, 'maintenance/asset_form.html', context)


@login_required
def asset_delete(request, pk):
    """Delete asset"""
    asset = get_object_or_404(Asset, pk=pk)
    
    if request.method == 'POST':
        asset.delete()
        messages.success(request, 'Asset deleted successfully!')
        return redirect('maintenance:asset_list')
    
    context = {'asset': asset}
    return render(request, 'maintenance/asset_confirm_delete.html', context)


# ==================== Preventive Maintenance Views ====================

@login_required
def pm_list(request):
    """List all preventive maintenances"""
    pms = PreventiveMaintenance.objects.select_related('asset', 'assigned_technician').all()
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        pms = pms.filter(status=status_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        pms = pms.filter(
            Q(pm_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(asset__asset_number__icontains=search_query)
        )
    
    context = {
        'pms': pms,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'maintenance/pm_list.html', context)


@login_required
def pm_detail(request, pk):
    """View preventive maintenance details"""
    pm = get_object_or_404(
        PreventiveMaintenance.objects.select_related(
            'asset', 'assigned_technician', 'created_by'
        ),
        pk=pk
    )
    
    # Get related work orders
    work_orders = pm.work_orders.all()[:10]
    
    context = {
        'pm': pm,
        'work_orders': work_orders,
    }
    return render(request, 'maintenance/pm_detail.html', context)


@login_required
def pm_create(request):
    """Create new preventive maintenance"""
    if request.method == 'POST':
        form = PreventiveMaintenanceForm(request.POST)
        if form.is_valid():
            pm = form.save(commit=False)
            pm.created_by = request.user
            pm.save()
            messages.success(request, f'Preventive Maintenance {pm.pm_number} created successfully!')
            return redirect('maintenance:pm_detail', pk=pm.pk)
    else:
        form = PreventiveMaintenanceForm()
    
    context = {'form': form}
    return render(request, 'maintenance/pm_form.html', context)


@login_required
def pm_update(request, pk):
    """Update preventive maintenance"""
    pm = get_object_or_404(PreventiveMaintenance, pk=pk)
    
    if request.method == 'POST':
        form = PreventiveMaintenanceForm(request.POST, instance=pm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Preventive Maintenance updated successfully!')
            return redirect('maintenance:pm_detail', pk=pm.pk)
    else:
        form = PreventiveMaintenanceForm(instance=pm)
    
    context = {
        'form': form,
        'pm': pm,
    }
    return render(request, 'maintenance/pm_form.html', context)


@login_required
def pm_delete(request, pk):
    """Delete preventive maintenance"""
    pm = get_object_or_404(PreventiveMaintenance, pk=pk)
    
    if request.method == 'POST':
        pm.delete()
        messages.success(request, 'Preventive Maintenance deleted successfully!')
        return redirect('maintenance:pm_list')
    
    context = {'pm': pm}
    return render(request, 'maintenance/pm_confirm_delete.html', context)


# ==================== Work Order Views ====================

@login_required
def workorder_list(request):
    """List all work orders"""
    work_orders = WorkOrder.objects.select_related(
        'asset', 'assigned_to', 'supervisor'
    ).all()
    
    # Filtering
    status_filter = request.GET.get('status')
    if status_filter:
        work_orders = work_orders.filter(status=status_filter)
    
    priority_filter = request.GET.get('priority')
    if priority_filter:
        work_orders = work_orders.filter(priority=priority_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        work_orders = work_orders.filter(
            Q(wo_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(asset__asset_number__icontains=search_query)
        )
    
    context = {
        'work_orders': work_orders,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'search_query': search_query,
    }
    return render(request, 'maintenance/workorder_list.html', context)


@login_required
def workorder_detail(request, pk):
    """View work order details"""
    wo = get_object_or_404(
        WorkOrder.objects.select_related(
            'asset', 'preventive_maintenance', 'assigned_to',
            'supervisor', 'requested_by', 'created_by'
        ).prefetch_related('assigned_team', 'logs'),
        pk=pk
    )
    
    context = {'wo': wo}
    return render(request, 'maintenance/workorder_detail.html', context)


@login_required
def workorder_create(request):
    """Create new work order"""
    if request.method == 'POST':
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            wo = form.save(commit=False)
            wo.requested_by = request.user
            wo.created_by = request.user
            wo.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, f'Work Order {wo.wo_number} created successfully!')
            return redirect('maintenance:workorder_detail', pk=wo.pk)
    else:
        form = WorkOrderForm()
    
    context = {'form': form}
    return render(request, 'maintenance/workorder_form.html', context)


@login_required
def workorder_update(request, pk):
    """Update work order"""
    wo = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        form = WorkOrderForm(request.POST, instance=wo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Order updated successfully!')
            return redirect('maintenance:workorder_detail', pk=wo.pk)
    else:
        form = WorkOrderForm(instance=wo)
    
    context = {
        'form': form,
        'wo': wo,
    }
    return render(request, 'maintenance/workorder_form.html', context)


@login_required
def workorder_delete(request, pk):
    """Delete work order"""
    wo = get_object_or_404(WorkOrder, pk=pk)
    
    if request.method == 'POST':
        wo.delete()
        messages.success(request, 'Work Order deleted successfully!')
        return redirect('maintenance:workorder_list')
    
    context = {'wo': wo}
    return render(request, 'maintenance/workorder_confirm_delete.html', context)


# ==================== Maintenance Log Views ====================

@login_required
def log_list(request):
    """List all maintenance logs"""
    logs = MaintenanceLog.objects.select_related(
        'asset', 'work_order', 'technician'
    ).all()
    
    # Filtering
    asset_filter = request.GET.get('asset')
    if asset_filter:
        logs = logs.filter(asset_id=asset_filter)
    
    search_query = request.GET.get('search')
    if search_query:
        logs = logs.filter(
            Q(title__icontains=search_query) |
            Q(asset__asset_number__icontains=search_query)
        )
    
    context = {
        'logs': logs,
        'search_query': search_query,
    }
    return render(request, 'maintenance/log_list.html', context)


@login_required
def log_create(request):
    """Create new maintenance log"""
    if request.method == 'POST':
        form = MaintenanceLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.created_by = request.user
            log.save()
            messages.success(request, 'Maintenance Log created successfully!')
            return redirect('maintenance:log_list')
    else:
        form = MaintenanceLogForm()
    
    context = {'form': form}
    return render(request, 'maintenance/log_form.html', context)
