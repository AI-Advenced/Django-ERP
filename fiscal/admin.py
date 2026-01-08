from django.contrib import admin
from .models import TaxRate, FiscalYear, Invoice, InvoiceItem, Payment, TaxReport


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_type', 'rate', 'country', 'is_active', 'effective_date', 'created_at']
    list_filter = ['tax_type', 'is_active', 'country']
    search_fields = ['name', 'description']
    date_hierarchy = 'effective_date'
    ordering = ['-created_at']


@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'status', 'created_by', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'description']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'unit_price', 'tax_rate', 'discount_percent', 'line_total']
    readonly_fields = ['line_total']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_type', 'customer_name', 'total_amount', 'status', 'invoice_date', 'created_at']
    list_filter = ['invoice_type', 'status', 'invoice_date']
    search_fields = ['invoice_number', 'customer_name', 'customer_email']
    date_hierarchy = 'invoice_date'
    ordering = ['-invoice_date']
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'invoice_type', 'invoice_date', 'due_date', 'status')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_address', 'customer_tax_id')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount', 'paid_amount', 'balance')
        }),
        ('Additional Information', {
            'fields': ('fiscal_year', 'notes', 'terms_conditions', 'created_by')
        }),
    )
    readonly_fields = ['balance', 'created_by']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_number', 'invoice', 'amount', 'payment_method', 'status', 'payment_date', 'created_at']
    list_filter = ['payment_method', 'status', 'payment_date']
    search_fields = ['payment_number', 'reference_number']
    date_hierarchy = 'payment_date'
    ordering = ['-payment_date']


@admin.register(TaxReport)
class TaxReportAdmin(admin.ModelAdmin):
    list_display = ['report_number', 'report_type', 'fiscal_year', 'period_start', 'period_end', 'net_tax', 'status', 'created_at']
    list_filter = ['report_type', 'status']
    search_fields = ['report_number']
    date_hierarchy = 'period_end'
    ordering = ['-period_end']
    readonly_fields = ['net_tax']
