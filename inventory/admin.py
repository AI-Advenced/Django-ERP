from django.contrib import admin
from .models import Product, Category, Unit, Location, StockMovement, ProductLocation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'description']
    search_fields = ['name', 'symbol']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'current_stock', 'minimum_stock', 
                    'cost_price', 'selling_price', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'track_inventory', 'created_at']
    search_fields = ['code', 'name', 'barcode', 'sku']
    date_hierarchy = 'created_at'
    raw_id_fields = ['created_by']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description', 'category', 'unit', 'is_active')
        }),
        ('Pricing', {
            'fields': ('cost_price', 'selling_price')
        }),
        ('Inventory', {
            'fields': ('track_inventory', 'current_stock', 'minimum_stock', 'maximum_stock')
        }),
        ('Additional Details', {
            'fields': ('barcode', 'sku', 'manufacturer', 'brand'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_default', 'is_active', 'created_at']
    list_filter = ['is_default', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'address']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['id', 'movement_type', 'product', 'quantity', 'location_from', 
                    'location_to', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['product__code', 'product__name', 'reference']
    date_hierarchy = 'created_at'
    raw_id_fields = ['product', 'created_by']
    readonly_fields = ['stock_before', 'stock_after', 'created_at']


@admin.register(ProductLocation)
class ProductLocationAdmin(admin.ModelAdmin):
    list_display = ['product', 'location', 'quantity', 'last_updated']
    list_filter = ['location', 'last_updated']
    search_fields = ['product__code', 'product__name', 'location__name']
    raw_id_fields = ['product', 'location']
