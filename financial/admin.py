from django.contrib import admin
from .models import (
    Account, Customer, Invoice, InvoiceItem, Bill, Payment,
    JournalEntry, JournalEntryLine, Expense, Budget
)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    fields = ['description', 'quantity', 'unit_price', 'total_price']
    readonly_fields = ['total_price']


class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 2
    fields = ['account', 'debit_amount', 'credit_amount', 'description']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'account_type', 'parent', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active']
    search_fields = ['code', 'name', 'description']
    ordering = ['code']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'company', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['is_active', 'city', 'country']
    search_fields = ['name', 'email', 'company', 'tax_id']
    ordering = ['name']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'invoice_date', 'due_date', 'status', 'total_amount', 'created_by']
    list_filter = ['status', 'invoice_date', 'due_date']
    search_fields = ['invoice_number', 'customer__name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [InvoiceItemInline]
    ordering = ['-invoice_date']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_number', 'vendor_name', 'bill_date', 'due_date', 'status', 'total_amount', 'created_by']
    list_filter = ['status', 'bill_date', 'due_date']
    search_fields = ['bill_number', 'vendor_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-bill_date']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_number', 'payment_type', 'payment_date', 'amount', 'payment_method', 'customer', 'created_by']
    list_filter = ['payment_type', 'payment_method', 'payment_date']
    search_fields = ['payment_number', 'reference_number']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-payment_date']


@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_number', 'entry_date', 'status', 'description', 'created_by']
    list_filter = ['status', 'entry_date']
    search_fields = ['entry_number', 'description']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [JournalEntryLineInline]
    ordering = ['-entry_date']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['expense_number', 'expense_date', 'category', 'amount', 'vendor_name', 'payment_method', 'created_by']
    list_filter = ['category', 'payment_method', 'expense_date', 'is_billable']
    search_fields = ['expense_number', 'vendor_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-expense_date']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['name', 'period_type', 'start_date', 'end_date', 'account', 'budgeted_amount', 'actual_amount', 'is_active']
    list_filter = ['period_type', 'is_active', 'start_date']
    search_fields = ['name', 'account__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-start_date']
