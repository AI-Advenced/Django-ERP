"""
Django admin configuration for Logistics & Supply Chain Management Module
"""
from django.contrib import admin
from .models import (
    Warehouse, Inventory, Shipment, ShipmentItem,
    Route, Delivery, StockMovement
)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    """Admin for Warehouse model"""
    list_display = ['code', 'name', 'warehouse_type', 'city', 'country', 
                    'total_capacity', 'current_utilization', 'is_active']
    list_filter = ['warehouse_type', 'is_active', 'country', 'city']
    search_fields = ['code', 'name', 'city', 'manager_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'warehouse_type', 'is_active')
        }),
        ('Location', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Capacity', {
            'fields': ('total_capacity', 'current_utilization')
        }),
        ('Contact', {
            'fields': ('manager_name', 'contact_email', 'contact_phone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Admin for Inventory model"""
    list_display = ['product_code', 'product_name', 'warehouse', 'quantity_on_hand',
                    'quantity_available', 'reorder_level', 'unit_cost', 'total_value']
    list_filter = ['warehouse', 'category']
    search_fields = ['product_code', 'product_name', 'description']
    readonly_fields = ['quantity_available', 'total_value', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('warehouse', 'product_code', 'product_name', 
                      'description', 'category', 'bin_location')
        }),
        ('Stock Levels', {
            'fields': ('quantity_on_hand', 'quantity_reserved', 'quantity_available',
                      'reorder_level', 'reorder_quantity')
        }),
        ('Valuation', {
            'fields': ('unit_cost', 'total_value')
        }),
        ('Other', {
            'fields': ('last_count_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Calculate totals before saving"""
        obj.update_totals()
        super().save_model(request, obj, form, change)


class ShipmentItemInline(admin.TabularInline):
    """Inline for shipment items"""
    model = ShipmentItem
    extra = 1
    fields = ['product_code', 'product_name', 'quantity_shipped', 'quantity_received',
              'unit_of_measure', 'package_count', 'weight', 'unit_price', 'line_total']
    readonly_fields = ['line_total']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """Admin for Shipment model"""
    list_display = ['shipment_number', 'shipment_type', 'status', 'origin_warehouse',
                    'destination_warehouse', 'carrier_name', 'scheduled_ship_date',
                    'estimated_delivery_date']
    list_filter = ['shipment_type', 'status', 'transport_mode', 'carrier_name']
    search_fields = ['shipment_number', 'tracking_number', 'carrier_name', 
                    'reference_document']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ShipmentItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('shipment_number', 'shipment_type', 'status', 'reference_document')
        }),
        ('Origin & Destination', {
            'fields': ('origin_warehouse', 'destination_warehouse')
        }),
        ('Shipping Details', {
            'fields': ('carrier_name', 'transport_mode', 'tracking_number')
        }),
        ('Schedule', {
            'fields': ('scheduled_ship_date', 'actual_ship_date',
                      'estimated_delivery_date', 'actual_delivery_date')
        }),
        ('Financial', {
            'fields': ('shipping_cost', 'insurance_cost', 'total_value')
        }),
        ('Additional Information', {
            'fields': ('notes', 'special_instructions'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ShipmentItem)
class ShipmentItemAdmin(admin.ModelAdmin):
    """Admin for ShipmentItem model"""
    list_display = ['shipment', 'product_code', 'product_name', 'quantity_shipped',
                    'quantity_received', 'unit_of_measure', 'unit_price', 'line_total']
    list_filter = ['shipment__shipment_type', 'unit_of_measure']
    search_fields = ['product_code', 'product_name', 'shipment__shipment_number']
    readonly_fields = ['line_total']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Admin for Route model"""
    list_display = ['route_code', 'route_name', 'status', 'start_warehouse',
                    'total_distance', 'estimated_cost']
    list_filter = ['status', 'start_warehouse']
    search_fields = ['route_code', 'route_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('route_code', 'route_name', 'status', 'start_warehouse', 'description')
        }),
        ('Metrics', {
            'fields': ('total_distance', 'estimated_duration', 'estimated_cost', 'frequency')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    """Admin for Delivery model"""
    list_display = ['delivery_number', 'status', 'route', 'shipment', 
                    'scheduled_date', 'driver_name', 'vehicle_number']
    list_filter = ['status', 'route', 'scheduled_date']
    search_fields = ['delivery_number', 'delivery_contact', 'driver_name', 'vehicle_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('delivery_number', 'status', 'route', 'shipment')
        }),
        ('Delivery Details', {
            'fields': ('delivery_address', 'delivery_contact', 'delivery_phone')
        }),
        ('Schedule', {
            'fields': ('scheduled_date', 'actual_start_time', 'actual_end_time')
        }),
        ('Driver & Vehicle', {
            'fields': ('driver_name', 'vehicle_number')
        }),
        ('Proof of Delivery', {
            'fields': ('signature', 'delivery_photo_url', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    """Admin for StockMovement model"""
    list_display = ['movement_number', 'movement_type', 'movement_date', 'inventory',
                    'quantity', 'unit_cost', 'total_cost', 'reference_document']
    list_filter = ['movement_type', 'movement_date', 'inventory__warehouse']
    search_fields = ['movement_number', 'reference_document', 'inventory__product_code']
    readonly_fields = ['total_cost', 'created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('movement_number', 'movement_type', 'movement_date', 'inventory')
        }),
        ('Quantity', {
            'fields': ('quantity', 'unit_of_measure', 'unit_cost', 'total_cost')
        }),
        ('References', {
            'fields': ('reference_document', 'shipment')
        }),
        ('Transfer Information', {
            'fields': ('from_warehouse', 'to_warehouse'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('reason', 'notes', 'created_by'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Calculate total before saving"""
        obj.calculate_total()
        if not obj.created_by:
            obj.created_by = request.user.username
        super().save_model(request, obj, form, change)
