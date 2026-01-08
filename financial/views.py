from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Sum, Count
from decimal import Decimal
from datetime import datetime, timedelta

from .models import (
    Account, Customer, Invoice, InvoiceItem, Bill, Payment,
    JournalEntry, JournalEntryLine, Expense, Budget
)


# ==================== DASHBOARD ====================

@login_required
def financial_dashboard(request):
    """Financial dashboard with key metrics"""
    # Calculate metrics
    total_revenue = Invoice.objects.filter(status='paid').aggregate(
        total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    total_expenses = Expense.objects.aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    
    accounts_receivable = Invoice.objects.filter(
        status__in=['sent', 'overdue']).aggregate(
        total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    accounts_payable = Bill.objects.filter(
        status__in=['pending', 'overdue']).aggregate(
        total=Sum('total_amount'))['total'] or Decimal('0.00')
    
    # Recent transactions
    recent_invoices = Invoice.objects.select_related('customer').order_by('-invoice_date')[:5]
    recent_payments = Payment.objects.order_by('-payment_date')[:5]
    recent_expenses = Expense.objects.order_by('-expense_date')[:5]
    
    # Status counts
    invoice_counts = Invoice.objects.values('status').annotate(count=Count('id'))
    
    context = {
        'total_revenue': total_revenue,
        'total_expenses': total_expenses,
        'net_profit': total_revenue - total_expenses,
        'accounts_receivable': accounts_receivable,
        'accounts_payable': accounts_payable,
        'recent_invoices': recent_invoices,
        'recent_payments': recent_payments,
        'recent_expenses': recent_expenses,
        'invoice_counts': invoice_counts,
    }
    
    return render(request, 'financial/dashboard.html', context)


# ==================== ACCOUNTS ====================

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'financial/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = Account.objects.all()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(name__icontains=search)
            )
        
        # Filter by type
        account_type = self.request.GET.get('account_type')
        if account_type:
            queryset = queryset.filter(account_type=account_type)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_accounts': Account.objects.count(),
            'active_accounts': Account.objects.filter(is_active=True).count(),
        }
        return context


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'financial/account_detail.html'
    context_object_name = 'account'


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    template_name = 'financial/account_form.html'
    fields = ['code', 'name', 'account_type', 'parent', 'description', 'is_active']
    success_url = reverse_lazy('financial:account_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Account created successfully!')
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'financial/account_form.html'
    fields = ['code', 'name', 'account_type', 'parent', 'description', 'is_active']
    success_url = reverse_lazy('financial:account_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Account updated successfully!')
        return super().form_valid(form)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'financial/account_confirm_delete.html'
    success_url = reverse_lazy('financial:account_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Account deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== CUSTOMERS ====================

class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'financial/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Customer.objects.all()
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(company__icontains=search)
            )
        
        return queryset


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'financial/customer_detail.html'
    context_object_name = 'customer'


class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'financial/customer_form.html'
    fields = ['name', 'email', 'phone', 'company', 'address', 'city', 'country', 'tax_id', 'credit_limit', 'notes', 'is_active']
    success_url = reverse_lazy('financial:customer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer created successfully!')
        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    template_name = 'financial/customer_form.html'
    fields = ['name', 'email', 'phone', 'company', 'address', 'city', 'country', 'tax_id', 'credit_limit', 'notes', 'is_active']
    success_url = reverse_lazy('financial:customer_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, DeleteView):
    model = Customer
    template_name = 'financial/customer_confirm_delete.html'
    success_url = reverse_lazy('financial:customer_list')


# ==================== INVOICES ====================

class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'financial/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Invoice.objects.select_related('customer').all()
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search) |
                Q(customer__name__icontains=search)
            )
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_invoices': Invoice.objects.count(),
            'draft': Invoice.objects.filter(status='draft').count(),
            'sent': Invoice.objects.filter(status='sent').count(),
            'paid': Invoice.objects.filter(status='paid').count(),
            'overdue': Invoice.objects.filter(status='overdue').count(),
            'total_amount': Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        }
        return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'financial/invoice_detail.html'
    context_object_name = 'invoice'


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = 'financial/invoice_form.html'
    fields = ['invoice_number', 'customer', 'invoice_date', 'due_date', 'status', 'tax_rate', 'discount_amount', 'notes', 'terms']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Invoice created successfully!')
        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = 'financial/invoice_form.html'
    fields = ['invoice_number', 'customer', 'invoice_date', 'due_date', 'status', 'tax_rate', 'discount_amount', 'notes', 'terms']
    
    def form_valid(self, form):
        messages.success(self.request, 'Invoice updated successfully!')
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'financial/invoice_confirm_delete.html'
    success_url = reverse_lazy('financial:invoice_list')


# ==================== BILLS ====================

class BillListView(LoginRequiredMixin, ListView):
    model = Bill
    template_name = 'financial/bill_list.html'
    context_object_name = 'bills'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_bills': Bill.objects.count(),
            'pending': Bill.objects.filter(status='pending').count(),
            'paid': Bill.objects.filter(status='paid').count(),
            'total_amount': Bill.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
        }
        return context


class BillDetailView(LoginRequiredMixin, DetailView):
    model = Bill
    template_name = 'financial/bill_detail.html'
    context_object_name = 'bill'


class BillCreateView(LoginRequiredMixin, CreateView):
    model = Bill
    template_name = 'financial/bill_form.html'
    fields = ['bill_number', 'vendor_name', 'vendor_email', 'vendor_phone', 'bill_date', 'due_date', 'status', 'subtotal', 'tax_amount', 'total_amount', 'notes']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Bill created successfully!')
        return super().form_valid(form)


class BillUpdateView(LoginRequiredMixin, UpdateView):
    model = Bill
    template_name = 'financial/bill_form.html'
    fields = ['bill_number', 'vendor_name', 'vendor_email', 'vendor_phone', 'bill_date', 'due_date', 'status', 'subtotal', 'tax_amount', 'total_amount', 'notes']


class BillDeleteView(LoginRequiredMixin, DeleteView):
    model = Bill
    template_name = 'financial/bill_confirm_delete.html'
    success_url = reverse_lazy('financial:bill_list')


# ==================== PAYMENTS ====================

class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'financial/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_received': Payment.objects.filter(payment_type='received').aggregate(Sum('amount'))['amount__sum'] or 0,
            'total_made': Payment.objects.filter(payment_type='made').aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return context


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'financial/payment_detail.html'
    context_object_name = 'payment'


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = 'financial/payment_form.html'
    fields = ['payment_number', 'payment_type', 'payment_date', 'amount', 'payment_method', 'invoice', 'bill', 'customer', 'reference_number', 'notes']
    success_url = reverse_lazy('financial:payment_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Payment recorded successfully!')
        return super().form_valid(form)


class PaymentUpdateView(LoginRequiredMixin, UpdateView):
    model = Payment
    template_name = 'financial/payment_form.html'
    fields = ['payment_number', 'payment_type', 'payment_date', 'amount', 'payment_method', 'invoice', 'bill', 'customer', 'reference_number', 'notes']
    success_url = reverse_lazy('financial:payment_list')


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'financial/payment_confirm_delete.html'
    success_url = reverse_lazy('financial:payment_list')


# ==================== EXPENSES ====================

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'financial/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Expense.objects.all()
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_expenses': Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
            'this_month': Expense.objects.filter(
                expense_date__month=datetime.now().month).aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return context


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'financial/expense_detail.html'
    context_object_name = 'expense'


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    template_name = 'financial/expense_form.html'
    fields = ['expense_number', 'expense_date', 'category', 'amount', 'vendor_name', 'description', 'payment_method', 'receipt_number', 'notes', 'is_billable', 'customer']
    success_url = reverse_lazy('financial:expense_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Expense recorded successfully!')
        return super().form_valid(form)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    template_name = 'financial/expense_form.html'
    fields = ['expense_number', 'expense_date', 'category', 'amount', 'vendor_name', 'description', 'payment_method', 'receipt_number', 'notes', 'is_billable', 'customer']
    success_url = reverse_lazy('financial:expense_list')


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'financial/expense_confirm_delete.html'
    success_url = reverse_lazy('financial:expense_list')


# ==================== JOURNAL ENTRIES ====================

class JournalEntryListView(LoginRequiredMixin, ListView):
    model = JournalEntry
    template_name = 'financial/journal_entry_list.html'
    context_object_name = 'entries'
    paginate_by = 20


class JournalEntryDetailView(LoginRequiredMixin, DetailView):
    model = JournalEntry
    template_name = 'financial/journal_entry_detail.html'
    context_object_name = 'entry'


class JournalEntryCreateView(LoginRequiredMixin, CreateView):
    model = JournalEntry
    template_name = 'financial/journal_entry_form.html'
    fields = ['entry_number', 'entry_date', 'status', 'description', 'notes']
    success_url = reverse_lazy('financial:journal_entry_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Journal entry created successfully!')
        return super().form_valid(form)


class JournalEntryUpdateView(LoginRequiredMixin, UpdateView):
    model = JournalEntry
    template_name = 'financial/journal_entry_form.html'
    fields = ['entry_number', 'entry_date', 'status', 'description', 'notes']
    success_url = reverse_lazy('financial:journal_entry_list')


class JournalEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = JournalEntry
    template_name = 'financial/journal_entry_confirm_delete.html'
    success_url = reverse_lazy('financial:journal_entry_list')


# ==================== BUDGETS ====================

class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'financial/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 20


class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = 'financial/budget_detail.html'
    context_object_name = 'budget'


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = 'financial/budget_form.html'
    fields = ['name', 'period_type', 'start_date', 'end_date', 'account', 'budgeted_amount', 'actual_amount', 'notes', 'is_active']
    success_url = reverse_lazy('financial:budget_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Budget created successfully!')
        return super().form_valid(form)


class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = 'financial/budget_form.html'
    fields = ['name', 'period_type', 'start_date', 'end_date', 'account', 'budgeted_amount', 'actual_amount', 'notes', 'is_active']
    success_url = reverse_lazy('financial:budget_list')


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'financial/budget_confirm_delete.html'
    success_url = reverse_lazy('financial:budget_list')
