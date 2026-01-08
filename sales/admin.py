from django.contrib import admin
from .models import Customer, SalesOrder, SalesOrderItem, Quotation, QuotationItem


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1
    fields = ['product_name', 'product_code', 'quantity', 'unit_price', 'discount_percentage', 'tax_rate']


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1
    fields = ['product_name', 'product_code', 'quantity', 'unit_price', 'discount_percentage']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer_type', 'email', 'phone', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['customer_type', 'is_active', 'country', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company_name', 'tax_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'customer_type', 'email', 'phone', 'mobile')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Business Information', {
            'fields': ('company_name', 'tax_id', 'website')
        }),
        ('Financial', {
            'fields': ('credit_limit', 'payment_terms')
        }),
        ('Status & Notes', {
            'fields': ('is_active', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer', 'order_date', 'status', 'priority', 
                   'total_amount', 'paid_amount', 'created_at']
    list_filter = ['status', 'priority', 'order_date', 'created_at']
    search_fields = ['order_number', 'customer__name', 'sales_person']
    readonly_fields = ['created_at', 'updated_at', 'confirmed_date', 'delivered_date']
    inlines = [SalesOrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'order_date', 'expected_delivery_date',
                      'status', 'priority', 'sales_person')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'discount_percentage',
                      'discount_amount', 'shipping_cost', 'total_amount', 'paid_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_state',
                      'shipping_country', 'shipping_postal_code'),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'terms_conditions', 'internal_notes'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at', 'confirmed_date', 'delivered_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ['sales_order', 'product_name', 'product_code', 'quantity', 
                   'unit_price', 'line_total']
    list_filter = ['sales_order__order_date', 'created_at']
    search_fields = ['product_name', 'product_code', 'sales_order__order_number']


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_number', 'customer', 'quotation_date', 'valid_until',
                   'status', 'total_amount', 'created_at']
    list_filter = ['status', 'quotation_date', 'valid_until', 'created_at']
    search_fields = ['quotation_number', 'customer__name', 'sales_person']
    readonly_fields = ['created_at', 'updated_at', 'sent_date', 'converted_order']
    inlines = [QuotationItemInline]
    
    fieldsets = (
        ('Quotation Information', {
            'fields': ('quotation_number', 'customer', 'quotation_date', 'valid_until',
                      'status', 'sales_person')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'terms_conditions'),
            'classes': ('collapse',)
        }),
        ('Conversion', {
            'fields': ('converted_order',),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at', 'sent_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ['quotation', 'product_name', 'product_code', 'quantity',
                   'unit_price', 'line_total']
    list_filter = ['quotation__quotation_date', 'created_at']
    search_fields = ['product_name', 'product_code', 'quotation__quotation_number']
