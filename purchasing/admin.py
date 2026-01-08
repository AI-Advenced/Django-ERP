from django.contrib import admin
from .models import (
    Supplier, PurchaseRequisition, PurchaseRequisitionItem,
    PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem,
    RFQ, RFQItem, SupplierQuotation
)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Admin interface for Supplier model."""
    list_display = ['supplier_code', 'name', 'supplier_type', 'email', 'status', 'is_preferred', 'rating', 'total_orders']
    list_filter = ['status', 'supplier_type', 'is_preferred', 'payment_terms']
    search_fields = ['supplier_code', 'name', 'email', 'contact_person']
    readonly_fields = ['created_at', 'updated_at', 'total_orders', 'total_amount']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('supplier_code', 'name', 'supplier_type', 'status', 'is_preferred')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'country', 'postal_code')
        }),
        ('Business Details', {
            'fields': ('tax_number', 'registration_number')
        }),
        ('Financial Terms', {
            'fields': ('payment_terms', 'credit_limit', 'currency')
        }),
        ('Performance Metrics', {
            'fields': ('rating', 'total_orders', 'total_amount')
        }),
        ('Contact Person', {
            'fields': ('contact_person', 'contact_person_phone', 'contact_person_email')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class PurchaseRequisitionItemInline(admin.TabularInline):
    """Inline admin for Purchase Requisition Items."""
    model = PurchaseRequisitionItem
    extra = 1
    fields = ['item_number', 'description', 'quantity', 'unit_of_measure', 'estimated_unit_price', 'suggested_supplier']


@admin.register(PurchaseRequisition)
class PurchaseRequisitionAdmin(admin.ModelAdmin):
    """Admin interface for Purchase Requisition model."""
    list_display = ['requisition_number', 'title', 'requested_by', 'department', 'requisition_date', 'priority', 'status']
    list_filter = ['status', 'priority', 'requisition_date', 'department']
    search_fields = ['requisition_number', 'title', 'requested_by', 'department']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PurchaseRequisitionItemInline]
    date_hierarchy = 'requisition_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('requisition_number', 'title', 'requested_by', 'department')
        }),
        ('Dates', {
            'fields': ('requisition_date', 'required_by_date')
        }),
        ('Priority and Status', {
            'fields': ('priority', 'status', 'estimated_total')
        }),
        ('Justification', {
            'fields': ('purpose', 'notes')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_date', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class PurchaseOrderItemInline(admin.TabularInline):
    """Inline admin for Purchase Order Items."""
    model = PurchaseOrderItem
    extra = 1
    fields = ['item_number', 'description', 'quantity_ordered', 'quantity_received', 'unit_of_measure', 'unit_price']
    readonly_fields = ['quantity_received']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    """Admin interface for Purchase Order model."""
    list_display = ['po_number', 'supplier', 'po_date', 'status', 'total_amount', 'expected_delivery_date']
    list_filter = ['status', 'po_date', 'expected_delivery_date']
    search_fields = ['po_number', 'supplier__name', 'supplier__supplier_code']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PurchaseOrderItemInline]
    date_hierarchy = 'po_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('po_number', 'supplier', 'requisition', 'created_by')
        }),
        ('Dates', {
            'fields': ('po_date', 'expected_delivery_date', 'actual_delivery_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'shipping_cost', 'other_charges', 'discount_amount', 'total_amount')
        }),
        ('Delivery Information', {
            'fields': ('delivery_address', 'delivery_contact', 'delivery_phone')
        }),
        ('Payment Terms', {
            'fields': ('payment_terms',)
        }),
        ('Notes', {
            'fields': ('notes', 'supplier_notes')
        }),
        ('Terms and Conditions', {
            'fields': ('terms_conditions',)
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class GoodsReceiptItemInline(admin.TabularInline):
    """Inline admin for Goods Receipt Items."""
    model = GoodsReceiptItem
    extra = 1
    fields = ['po_item', 'quantity_received', 'quantity_accepted', 'quantity_rejected', 'condition']


@admin.register(GoodsReceipt)
class GoodsReceiptAdmin(admin.ModelAdmin):
    """Admin interface for Goods Receipt model."""
    list_display = ['grn_number', 'purchase_order', 'receipt_date', 'received_by', 'status']
    list_filter = ['status', 'receipt_date']
    search_fields = ['grn_number', 'purchase_order__po_number']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [GoodsReceiptItemInline]
    date_hierarchy = 'receipt_date'


class RFQItemInline(admin.TabularInline):
    """Inline admin for RFQ Items."""
    model = RFQItem
    extra = 1
    fields = ['item_number', 'description', 'quantity', 'unit_of_measure']


@admin.register(RFQ)
class RFQAdmin(admin.ModelAdmin):
    """Admin interface for RFQ model."""
    list_display = ['rfq_number', 'title', 'rfq_date', 'submission_deadline', 'status']
    list_filter = ['status', 'rfq_date']
    search_fields = ['rfq_number', 'title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [RFQItemInline]
    date_hierarchy = 'rfq_date'


@admin.register(SupplierQuotation)
class SupplierQuotationAdmin(admin.ModelAdmin):
    """Admin interface for Supplier Quotation model."""
    list_display = ['quotation_number', 'supplier', 'rfq', 'quotation_date', 'status', 'total_amount', 'evaluation_score']
    list_filter = ['status', 'quotation_date']
    search_fields = ['quotation_number', 'supplier__name', 'rfq__rfq_number']
    readonly_fields = ['created_at', 'updated_at']
