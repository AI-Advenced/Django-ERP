from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import (
    Supplier, PurchaseRequisition, PurchaseRequisitionItem,
    PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem,
    RFQ, RFQItem, SupplierQuotation
)


# Dashboard View
class PurchasingDashboardView(TemplateView):
    """
    Dashboard view showing purchasing & procurement metrics and statistics.
    """
    template_name = 'purchasing/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Active Suppliers
        context['active_suppliers_count'] = Supplier.objects.filter(status='active').count()
        
        # Purchase Orders Statistics
        context['total_pos'] = PurchaseOrder.objects.count()
        context['pending_pos'] = PurchaseOrder.objects.filter(
            status__in=['draft', 'sent', 'acknowledged']
        ).count()
        
        # Purchase Requisitions Statistics
        context['pending_requisitions'] = PurchaseRequisition.objects.filter(
            status__in=['draft', 'submitted']
        ).count()
        
        # Total Spend (last 30 days)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        context['total_spend'] = PurchaseOrder.objects.filter(
            po_date__gte=thirty_days_ago,
            status__in=['sent', 'acknowledged', 'partially_received', 'received']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Recent Purchase Orders
        context['recent_pos'] = PurchaseOrder.objects.select_related('supplier').order_by('-created_at')[:5]
        
        # Recent Requisitions
        context['recent_requisitions'] = PurchaseRequisition.objects.order_by('-created_at')[:5]
        
        # Pending Goods Receipts
        context['pending_receipts'] = GoodsReceipt.objects.filter(
            status__in=['draft', 'received']
        ).count()
        
        # Top Suppliers by order volume
        context['top_suppliers'] = Supplier.objects.filter(
            status='active'
        ).order_by('-total_orders')[:5]
        
        return context


# Supplier Views
class SupplierListView(ListView):
    """List all suppliers with search and filter."""
    model = Supplier
    template_name = 'purchasing/supplier_list.html'
    context_object_name = 'suppliers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(supplier_code__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by type
        supplier_type = self.request.GET.get('type')
        if supplier_type:
            queryset = queryset.filter(supplier_type=supplier_type)
        
        return queryset


class SupplierDetailView(DetailView):
    """Detail view for a supplier."""
    model = Supplier
    template_name = 'purchasing/supplier_detail.html'
    context_object_name = 'supplier'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        supplier = self.get_object()
        
        # Recent Purchase Orders
        context['recent_orders'] = PurchaseOrder.objects.filter(
            supplier=supplier
        ).order_by('-po_date')[:10]
        
        # Statistics
        context['total_pos'] = supplier.purchase_orders.count()
        context['total_spend'] = supplier.purchase_orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        return context


class SupplierCreateView(CreateView):
    """Create a new supplier."""
    model = Supplier
    template_name = 'purchasing/supplier_form.html'
    fields = [
        'supplier_code', 'name', 'supplier_type', 'email', 'phone', 'website',
        'address', 'city', 'state', 'country', 'postal_code',
        'tax_number', 'registration_number', 'payment_terms', 'credit_limit',
        'currency', 'status', 'is_preferred', 'notes',
        'contact_person', 'contact_person_phone', 'contact_person_email'
    ]
    success_url = reverse_lazy('purchasing:supplier_list')


class SupplierUpdateView(UpdateView):
    """Update supplier information."""
    model = Supplier
    template_name = 'purchasing/supplier_form.html'
    fields = [
        'supplier_code', 'name', 'supplier_type', 'email', 'phone', 'website',
        'address', 'city', 'state', 'country', 'postal_code',
        'tax_number', 'registration_number', 'payment_terms', 'credit_limit',
        'currency', 'status', 'is_preferred', 'notes', 'rating',
        'contact_person', 'contact_person_phone', 'contact_person_email'
    ]
    success_url = reverse_lazy('purchasing:supplier_list')


class SupplierDeleteView(DeleteView):
    """Delete a supplier."""
    model = Supplier
    template_name = 'purchasing/supplier_confirm_delete.html'
    success_url = reverse_lazy('purchasing:supplier_list')


# Purchase Requisition Views
class RequisitionListView(ListView):
    """List all purchase requisitions."""
    model = PurchaseRequisition
    template_name = 'purchasing/requisition_list.html'
    context_object_name = 'requisitions'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        return queryset


class RequisitionDetailView(DetailView):
    """Detail view for a purchase requisition."""
    model = PurchaseRequisition
    template_name = 'purchasing/requisition_detail.html'
    context_object_name = 'requisition'


class RequisitionCreateView(CreateView):
    """Create a new purchase requisition."""
    model = PurchaseRequisition
    template_name = 'purchasing/requisition_form.html'
    fields = [
        'requisition_number', 'title', 'requested_by', 'department',
        'requisition_date', 'required_by_date', 'priority', 'purpose', 'notes'
    ]
    success_url = reverse_lazy('purchasing:requisition_list')


class RequisitionUpdateView(UpdateView):
    """Update a purchase requisition."""
    model = PurchaseRequisition
    template_name = 'purchasing/requisition_form.html'
    fields = [
        'requisition_number', 'title', 'requested_by', 'department',
        'requisition_date', 'required_by_date', 'priority', 'status',
        'purpose', 'notes', 'approved_by', 'rejection_reason'
    ]
    success_url = reverse_lazy('purchasing:requisition_list')


class RequisitionDeleteView(DeleteView):
    """Delete a purchase requisition."""
    model = PurchaseRequisition
    template_name = 'purchasing/requisition_confirm_delete.html'
    success_url = reverse_lazy('purchasing:requisition_list')


# Purchase Order Views
class PurchaseOrderListView(ListView):
    """List all purchase orders."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_list.html'
    context_object_name = 'purchase_orders'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('supplier')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(po_number__icontains=search) |
                Q(supplier__name__icontains=search)
            )
        
        return queryset


class PurchaseOrderDetailView(DetailView):
    """Detail view for a purchase order."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_detail.html'
    context_object_name = 'purchase_order'


class PurchaseOrderCreateView(CreateView):
    """Create a new purchase order."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_form.html'
    fields = [
        'po_number', 'supplier', 'requisition', 'po_date', 'expected_delivery_date',
        'delivery_address', 'delivery_contact', 'delivery_phone',
        'payment_terms', 'notes', 'supplier_notes', 'terms_conditions', 'created_by'
    ]
    success_url = reverse_lazy('purchasing:purchase_order_list')


class PurchaseOrderUpdateView(UpdateView):
    """Update a purchase order."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_form.html'
    fields = [
        'po_number', 'supplier', 'po_date', 'expected_delivery_date', 'status',
        'delivery_address', 'delivery_contact', 'delivery_phone',
        'payment_terms', 'notes', 'supplier_notes', 'terms_conditions',
        'approved_by'
    ]
    success_url = reverse_lazy('purchasing:purchase_order_list')


class PurchaseOrderDeleteView(DeleteView):
    """Delete a purchase order."""
    model = PurchaseOrder
    template_name = 'purchasing/purchase_order_confirm_delete.html'
    success_url = reverse_lazy('purchasing:purchase_order_list')


# Goods Receipt Views
class GoodsReceiptListView(ListView):
    """List all goods receipts."""
    model = GoodsReceipt
    template_name = 'purchasing/goods_receipt_list.html'
    context_object_name = 'receipts'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('purchase_order', 'purchase_order__supplier')
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


class GoodsReceiptDetailView(DetailView):
    """Detail view for a goods receipt."""
    model = GoodsReceipt
    template_name = 'purchasing/goods_receipt_detail.html'
    context_object_name = 'receipt'


class GoodsReceiptCreateView(CreateView):
    """Create a new goods receipt."""
    model = GoodsReceipt
    template_name = 'purchasing/goods_receipt_form.html'
    fields = [
        'grn_number', 'purchase_order', 'receipt_date', 'received_by',
        'delivery_note_number', 'vehicle_number', 'driver_name', 'notes'
    ]
    success_url = reverse_lazy('purchasing:goods_receipt_list')


class GoodsReceiptUpdateView(UpdateView):
    """Update a goods receipt."""
    model = GoodsReceipt
    template_name = 'purchasing/goods_receipt_form.html'
    fields = [
        'grn_number', 'receipt_date', 'received_by', 'status',
        'delivery_note_number', 'vehicle_number', 'driver_name',
        'inspected_by', 'inspection_date', 'inspection_notes',
        'notes', 'rejection_reason'
    ]
    success_url = reverse_lazy('purchasing:goods_receipt_list')


class GoodsReceiptDeleteView(DeleteView):
    """Delete a goods receipt."""
    model = GoodsReceipt
    template_name = 'purchasing/goods_receipt_confirm_delete.html'
    success_url = reverse_lazy('purchasing:goods_receipt_list')


# RFQ Views
class RFQListView(ListView):
    """List all RFQs."""
    model = RFQ
    template_name = 'purchasing/rfq_list.html'
    context_object_name = 'rfqs'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


class RFQDetailView(DetailView):
    """Detail view for an RFQ."""
    model = RFQ
    template_name = 'purchasing/rfq_detail.html'
    context_object_name = 'rfq'


class RFQCreateView(CreateView):
    """Create a new RFQ."""
    model = RFQ
    template_name = 'purchasing/rfq_form.html'
    fields = [
        'rfq_number', 'title', 'requisition', 'rfq_date', 'submission_deadline',
        'description', 'terms_conditions', 'notes', 'created_by'
    ]
    success_url = reverse_lazy('purchasing:rfq_list')


class RFQUpdateView(UpdateView):
    """Update an RFQ."""
    model = RFQ
    template_name = 'purchasing/rfq_form.html'
    fields = [
        'rfq_number', 'title', 'rfq_date', 'submission_deadline', 'status',
        'description', 'terms_conditions', 'notes'
    ]
    success_url = reverse_lazy('purchasing:rfq_list')


class RFQDeleteView(DeleteView):
    """Delete an RFQ."""
    model = RFQ
    template_name = 'purchasing/rfq_confirm_delete.html'
    success_url = reverse_lazy('purchasing:rfq_list')
