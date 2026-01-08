from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.contrib import messages
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from datetime import timedelta

from .models import Customer, SalesOrder, SalesOrderItem, Quotation, QuotationItem
from .forms import (
    CustomerForm, SalesOrderForm, SalesOrderItemForm, 
    QuotationForm, QuotationItemForm
)


# Dashboard View
class SalesDashboardView(TemplateView):
    """
    Sales Dashboard with key metrics and charts
    """
    template_name = 'sales/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Current month
        now = timezone.now()
        first_day = now.replace(day=1)
        
        # Key Metrics
        context['total_customers'] = Customer.objects.filter(is_active=True).count()
        context['total_orders'] = SalesOrder.objects.count()
        context['pending_orders'] = SalesOrder.objects.filter(
            status__in=['draft', 'quotation', 'confirmed', 'processing']
        ).count()
        context['total_quotations'] = Quotation.objects.filter(status='sent').count()
        
        # Revenue
        context['total_revenue'] = SalesOrder.objects.filter(
            status__in=['delivered', 'invoiced']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        context['monthly_revenue'] = SalesOrder.objects.filter(
            status__in=['delivered', 'invoiced'],
            order_date__gte=first_day
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Recent Orders
        context['recent_orders'] = SalesOrder.objects.all()[:5]
        
        # Recent Quotations
        context['recent_quotations'] = Quotation.objects.all()[:5]
        
        # Top Customers
        context['top_customers'] = Customer.objects.annotate(
            total_sales=Sum('sales_orders__total_amount')
        ).order_by('-total_sales')[:5]
        
        # Orders by Status
        context['orders_by_status'] = SalesOrder.objects.values('status').annotate(
            count=Count('id')
        )
        
        return context


# ============ Customer Views ============

class CustomerListView(ListView):
    """
    List all customers
    """
    model = Customer
    template_name = 'sales/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone__icontains=search) |
                Q(company_name__icontains=search)
            )
        
        return queryset


class CustomerDetailView(DetailView):
    """
    Display customer details
    """
    model = Customer
    template_name = 'sales/customer_detail.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        # Customer's orders
        context['orders'] = customer.sales_orders.all()[:10]
        context['quotations'] = customer.quotations.all()[:10]
        
        # Statistics
        context['total_orders'] = customer.sales_orders.count()
        context['total_spent'] = customer.sales_orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        return context


class CustomerCreateView(CreateView):
    """
    Create new customer
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'sales/customer_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Customer created successfully!')
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    """
    Update existing customer
    """
    model = Customer
    form_class = CustomerForm
    template_name = 'sales/customer_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Customer updated successfully!')
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    """
    Delete customer
    """
    model = Customer
    template_name = 'sales/customer_confirm_delete.html'
    success_url = reverse_lazy('sales:customer_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Customer deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============ Sales Order Views ============

class SalesOrderListView(ListView):
    """
    List all sales orders
    """
    model = SalesOrder
    template_name = 'sales/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filters
        status = self.request.GET.get('status', '')
        search = self.request.GET.get('search', '')
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(customer__name__icontains=search)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = SalesOrder.STATUS_CHOICES
        return context


class SalesOrderDetailView(DetailView):
    """
    Display sales order details
    """
    model = SalesOrder
    template_name = 'sales/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        context['items'] = order.items.all()
        return context


class SalesOrderCreateView(CreateView):
    """
    Create new sales order
    """
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = 'sales/order_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Sales order created successfully!')
        return super().form_valid(form)


class SalesOrderUpdateView(UpdateView):
    """
    Update existing sales order
    """
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = 'sales/order_form.html'

    def form_valid(self, form):
        order = form.save(commit=False)
        order.calculate_totals()
        order.save()
        messages.success(self.request, 'Sales order updated successfully!')
        return super().form_valid(form)


class SalesOrderDeleteView(DeleteView):
    """
    Delete sales order
    """
    model = SalesOrder
    template_name = 'sales/order_confirm_delete.html'
    success_url = reverse_lazy('sales:order_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Sales order deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============ Quotation Views ============

class QuotationListView(ListView):
    """
    List all quotations
    """
    model = Quotation
    template_name = 'sales/quotation_list.html'
    context_object_name = 'quotations'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filters
        status = self.request.GET.get('status', '')
        search = self.request.GET.get('search', '')
        
        if status:
            queryset = queryset.filter(status=status)
        
        if search:
            queryset = queryset.filter(
                Q(quotation_number__icontains=search) |
                Q(customer__name__icontains=search)
            )
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Quotation.STATUS_CHOICES
        return context


class QuotationDetailView(DetailView):
    """
    Display quotation details
    """
    model = Quotation
    template_name = 'sales/quotation_detail.html'
    context_object_name = 'quotation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotation = self.get_object()
        context['items'] = quotation.items.all()
        return context


class QuotationCreateView(CreateView):
    """
    Create new quotation
    """
    model = Quotation
    form_class = QuotationForm
    template_name = 'sales/quotation_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Quotation created successfully!')
        return super().form_valid(form)


class QuotationUpdateView(UpdateView):
    """
    Update existing quotation
    """
    model = Quotation
    form_class = QuotationForm
    template_name = 'sales/quotation_form.html'

    def form_valid(self, form):
        quotation = form.save(commit=False)
        quotation.calculate_totals()
        quotation.save()
        messages.success(self.request, 'Quotation updated successfully!')
        return super().form_valid(form)


class QuotationDeleteView(DeleteView):
    """
    Delete quotation
    """
    model = Quotation
    template_name = 'sales/quotation_confirm_delete.html'
    success_url = reverse_lazy('sales:quotation_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Quotation deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ============ Convert Quotation to Order ============

def convert_quotation_to_order(request, pk):
    """
    Convert quotation to sales order
    """
    quotation = get_object_or_404(Quotation, pk=pk)
    
    if quotation.status == 'converted':
        messages.warning(request, 'This quotation has already been converted!')
        return redirect('sales:quotation_detail', pk=pk)
    
    # Create sales order from quotation
    order = SalesOrder.objects.create(
        order_number=f"SO-{quotation.quotation_number}",
        customer=quotation.customer,
        order_date=timezone.now().date(),
        status='confirmed',
        subtotal=quotation.subtotal,
        tax_rate=quotation.tax_rate,
        tax_amount=quotation.tax_amount,
        discount_amount=quotation.discount_amount,
        total_amount=quotation.total_amount,
        notes=quotation.notes,
        terms_conditions=quotation.terms_conditions,
        sales_person=quotation.sales_person,
    )
    
    # Copy items
    for item in quotation.items.all():
        SalesOrderItem.objects.create(
            sales_order=order,
            product_name=item.product_name,
            product_code=item.product_code,
            description=item.description,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount_percentage=item.discount_percentage,
        )
    
    # Update quotation
    quotation.status = 'converted'
    quotation.converted_order = order
    quotation.save()
    
    messages.success(request, f'Quotation converted to Sales Order #{order.order_number}')
    return redirect('sales:order_detail', pk=order.pk)
