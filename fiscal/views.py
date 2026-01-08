from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Sum
from .models import TaxRate, FiscalYear, Invoice, InvoiceItem, Payment, TaxReport
from datetime import datetime, date


# TaxRate Views
class TaxRateListView(LoginRequiredMixin, ListView):
    model = TaxRate
    template_name = 'fiscal/taxrate_list.html'
    context_object_name = 'taxrates'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TaxRate.objects.all()
        search = self.request.GET.get('search')
        tax_type = self.request.GET.get('tax_type')
        status = self.request.GET.get('status')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        if tax_type:
            queryset = queryset.filter(tax_type=tax_type)
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_rates': TaxRate.objects.count(),
            'active_rates': TaxRate.objects.filter(is_active=True).count(),
        }
        return context


class TaxRateDetailView(LoginRequiredMixin, DetailView):
    model = TaxRate
    template_name = 'fiscal/taxrate_detail.html'
    context_object_name = 'taxrate'


class TaxRateCreateView(LoginRequiredMixin, CreateView):
    model = TaxRate
    template_name = 'fiscal/taxrate_form.html'
    fields = ['name', 'tax_type', 'rate', 'description', 'country', 'is_active', 'effective_date', 'expiry_date']
    
    def form_valid(self, form):
        messages.success(self.request, 'Tax rate created successfully!')
        return super().form_valid(form)


class TaxRateUpdateView(LoginRequiredMixin, UpdateView):
    model = TaxRate
    template_name = 'fiscal/taxrate_form.html'
    fields = ['name', 'tax_type', 'rate', 'description', 'country', 'is_active', 'effective_date', 'expiry_date']
    
    def form_valid(self, form):
        messages.success(self.request, 'Tax rate updated successfully!')
        return super().form_valid(form)


class TaxRateDeleteView(LoginRequiredMixin, DeleteView):
    model = TaxRate
    template_name = 'fiscal/taxrate_confirm_delete.html'
    success_url = reverse_lazy('fiscal:taxrate_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tax rate deleted successfully!')
        return super().delete(request, *args, **kwargs)


# FiscalYear Views
class FiscalYearListView(LoginRequiredMixin, ListView):
    model = FiscalYear
    template_name = 'fiscal/fiscalyear_list.html'
    context_object_name = 'fiscal_years'
    paginate_by = 20


class FiscalYearDetailView(LoginRequiredMixin, DetailView):
    model = FiscalYear
    template_name = 'fiscal/fiscalyear_detail.html'
    context_object_name = 'fiscal_year'


class FiscalYearCreateView(LoginRequiredMixin, CreateView):
    model = FiscalYear
    template_name = 'fiscal/fiscalyear_form.html'
    fields = ['name', 'start_date', 'end_date', 'status', 'description']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Fiscal year created successfully!')
        return super().form_valid(form)


class FiscalYearUpdateView(LoginRequiredMixin, UpdateView):
    model = FiscalYear
    template_name = 'fiscal/fiscalyear_form.html'
    fields = ['name', 'start_date', 'end_date', 'status', 'description']
    
    def form_valid(self, form):
        messages.success(self.request, 'Fiscal year updated successfully!')
        return super().form_valid(form)


class FiscalYearDeleteView(LoginRequiredMixin, DeleteView):
    model = FiscalYear
    template_name = 'fiscal/fiscalyear_confirm_delete.html'
    success_url = reverse_lazy('fiscal:fiscalyear_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Fiscal year deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Invoice Views
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'fiscal/invoice_list.html'
    context_object_name = 'invoices'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Invoice.objects.all()
        search = self.request.GET.get('search')
        invoice_type = self.request.GET.get('invoice_type')
        status = self.request.GET.get('status')
        
        if search:
            queryset = queryset.filter(
                Q(invoice_number__icontains=search) |
                Q(customer_name__icontains=search)
            )
        if invoice_type:
            queryset = queryset.filter(invoice_type=invoice_type)
        if status:
            queryset = queryset.filter(status=status)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_invoices': Invoice.objects.count(),
            'total_amount': Invoice.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'paid_invoices': Invoice.objects.filter(status='paid').count(),
            'overdue_invoices': Invoice.objects.filter(status='overdue').count(),
        }
        return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'fiscal/invoice_detail.html'
    context_object_name = 'invoice'


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    template_name = 'fiscal/invoice_form.html'
    fields = ['invoice_number', 'invoice_type', 'invoice_date', 'due_date', 
              'customer_name', 'customer_email', 'customer_address', 'customer_tax_id',
              'subtotal', 'tax_amount', 'discount_amount', 'total_amount', 
              'status', 'notes', 'terms_conditions', 'fiscal_year']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Invoice created successfully!')
        return super().form_valid(form)


class InvoiceUpdateView(LoginRequiredMixin, UpdateView):
    model = Invoice
    template_name = 'fiscal/invoice_form.html'
    fields = ['invoice_number', 'invoice_type', 'invoice_date', 'due_date', 
              'customer_name', 'customer_email', 'customer_address', 'customer_tax_id',
              'subtotal', 'tax_amount', 'discount_amount', 'total_amount', 
              'status', 'notes', 'terms_conditions', 'fiscal_year']
    
    def form_valid(self, form):
        messages.success(self.request, 'Invoice updated successfully!')
        return super().form_valid(form)


class InvoiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Invoice
    template_name = 'fiscal/invoice_confirm_delete.html'
    success_url = reverse_lazy('fiscal:invoice_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Invoice deleted successfully!')
        return super().delete(request, *args, **kwargs)


# Payment Views
class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'fiscal/payment_list.html'
    context_object_name = 'payments'
    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stats'] = {
            'total_payments': Payment.objects.filter(status='completed').count(),
            'total_amount': Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0,
        }
        return context


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = 'fiscal/payment_detail.html'
    context_object_name = 'payment'


class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    template_name = 'fiscal/payment_form.html'
    fields = ['payment_number', 'invoice', 'payment_date', 'amount', 
              'payment_method', 'status', 'reference_number', 'notes']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Update invoice paid amount
        invoice = form.instance.invoice
        invoice.paid_amount += form.instance.amount
        invoice.save()
        
        messages.success(self.request, 'Payment recorded successfully!')
        return super().form_valid(form)


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = 'fiscal/payment_confirm_delete.html'
    success_url = reverse_lazy('fiscal:payment_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Payment deleted successfully!')
        return super().delete(request, *args, **kwargs)


# TaxReport Views
class TaxReportListView(LoginRequiredMixin, ListView):
    model = TaxReport
    template_name = 'fiscal/taxreport_list.html'
    context_object_name = 'tax_reports'
    paginate_by = 20


class TaxReportDetailView(LoginRequiredMixin, DetailView):
    model = TaxReport
    template_name = 'fiscal/taxreport_detail.html'
    context_object_name = 'tax_report'


class TaxReportCreateView(LoginRequiredMixin, CreateView):
    model = TaxReport
    template_name = 'fiscal/taxreport_form.html'
    fields = ['report_number', 'report_type', 'fiscal_year', 'period_start', 'period_end',
              'total_sales', 'total_purchases', 'tax_collected', 'tax_paid', 'status', 'notes']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Tax report created successfully!')
        return super().form_valid(form)


class TaxReportUpdateView(LoginRequiredMixin, UpdateView):
    model = TaxReport
    template_name = 'fiscal/taxreport_form.html'
    fields = ['report_number', 'report_type', 'fiscal_year', 'period_start', 'period_end',
              'total_sales', 'total_purchases', 'tax_collected', 'tax_paid', 'status', 'notes']
    
    def form_valid(self, form):
        messages.success(self.request, 'Tax report updated successfully!')
        return super().form_valid(form)


class TaxReportDeleteView(LoginRequiredMixin, DeleteView):
    model = TaxReport
    template_name = 'fiscal/taxreport_confirm_delete.html'
    success_url = reverse_lazy('fiscal:taxreport_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tax report deleted successfully!')
        return super().delete(request, *args, **kwargs)
