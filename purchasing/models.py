from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Supplier(models.Model):
    """
    Supplier/Vendor model for managing procurement sources.
    """
    SUPPLIER_TYPES = [
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
        ('wholesaler', 'Wholesaler'),
        ('service_provider', 'Service Provider'),
        ('contractor', 'Contractor'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blocked', 'Blocked'),
        ('pending_approval', 'Pending Approval'),
    ]
    
    PAYMENT_TERMS = [
        ('net_30', 'Net 30'),
        ('net_60', 'Net 60'),
        ('net_90', 'Net 90'),
        ('cod', 'Cash on Delivery'),
        ('advance', 'Advance Payment'),
        ('custom', 'Custom Terms'),
    ]
    
    # Basic Information
    supplier_code = models.CharField(max_length=50, unique=True, help_text='Unique supplier code')
    name = models.CharField(max_length=200)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPES, default='distributor')
    
    # Contact Information
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    website = models.URLField(blank=True, null=True)
    
    # Address
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Business Details
    tax_number = models.CharField(max_length=50, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    
    # Financial Terms
    payment_terms = models.CharField(max_length=20, choices=PAYMENT_TERMS, default='net_30')
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    
    # Performance Metrics
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    total_orders = models.IntegerField(default=0)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_preferred = models.BooleanField(default=False, help_text='Mark as preferred supplier')
    
    # Additional Information
    notes = models.TextField(blank=True)
    
    # Contact Person
    contact_person = models.CharField(max_length=100, blank=True)
    contact_person_phone = models.CharField(max_length=20, blank=True)
    contact_person_email = models.EmailField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return f"{self.supplier_code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('purchasing:supplier_detail', kwargs={'pk': self.pk})


class PurchaseRequisition(models.Model):
    """
    Purchase Requisition - Internal request to purchase items.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('converted', 'Converted to PO'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Basic Information
    requisition_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    
    # Requester Information
    requested_by = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    
    # Dates
    requisition_date = models.DateField()
    required_by_date = models.DateField(help_text='Date when items are needed')
    
    # Priority and Status
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Financial
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Justification
    purpose = models.TextField(help_text='Purpose of this requisition')
    notes = models.TextField(blank=True)
    
    # Approval
    approved_by = models.CharField(max_length=100, blank=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-requisition_date', '-created_at']
        verbose_name = 'Purchase Requisition'
        verbose_name_plural = 'Purchase Requisitions'
    
    def __str__(self):
        return f"{self.requisition_number} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('purchasing:requisition_detail', kwargs={'pk': self.pk})


class PurchaseRequisitionItem(models.Model):
    """
    Line items for Purchase Requisitions.
    """
    requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE, related_name='items')
    item_number = models.IntegerField(default=1)
    
    # Item Details
    description = models.CharField(max_length=500)
    specification = models.TextField(blank=True, help_text='Technical specifications')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_of_measure = models.CharField(max_length=50, default='pcs')
    
    # Pricing
    estimated_unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estimated_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Suggested Supplier
    suggested_supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['item_number']
        verbose_name = 'Requisition Item'
        verbose_name_plural = 'Requisition Items'
    
    def __str__(self):
        return f"{self.requisition.requisition_number} - Item {self.item_number}"
    
    def save(self, *args, **kwargs):
        """Calculate estimated total before saving."""
        self.estimated_total = self.quantity * self.estimated_unit_price
        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    """
    Purchase Order - Formal order sent to supplier.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent to Supplier'),
        ('acknowledged', 'Acknowledged'),
        ('partially_received', 'Partially Received'),
        ('received', 'Fully Received'),
        ('cancelled', 'Cancelled'),
        ('closed', 'Closed'),
    ]
    
    # Basic Information
    po_number = models.CharField(max_length=50, unique=True, verbose_name='PO Number')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    
    # Reference
    requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders')
    
    # Dates
    po_date = models.DateField(verbose_name='PO Date')
    expected_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Financial Details
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text='Tax rate in percentage')
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Delivery Information
    delivery_address = models.TextField()
    delivery_contact = models.CharField(max_length=100, blank=True)
    delivery_phone = models.CharField(max_length=20, blank=True)
    
    # Payment Terms
    payment_terms = models.CharField(max_length=200)
    
    # Notes
    notes = models.TextField(blank=True, help_text='Internal notes')
    supplier_notes = models.TextField(blank=True, help_text='Notes to supplier')
    
    # Terms and Conditions
    terms_conditions = models.TextField(blank=True, help_text='Terms and conditions')
    
    # Created By
    created_by = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=100, blank=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-po_date', '-created_at']
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
    
    def __str__(self):
        return f"{self.po_number} - {self.supplier.name}"
    
    def get_absolute_url(self):
        return reverse('purchasing:purchase_order_detail', kwargs={'pk': self.pk})


class PurchaseOrderItem(models.Model):
    """
    Line items for Purchase Orders.
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    item_number = models.IntegerField(default=1)
    
    # Item Details
    description = models.CharField(max_length=500)
    specification = models.TextField(blank=True)
    quantity_ordered = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_of_measure = models.CharField(max_length=50, default='pcs')
    
    # Pricing
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Delivery
    expected_delivery_date = models.DateField(blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['item_number']
        verbose_name = 'Purchase Order Item'
        verbose_name_plural = 'Purchase Order Items'
    
    def __str__(self):
        return f"{self.purchase_order.po_number} - Item {self.item_number}"
    
    def save(self, *args, **kwargs):
        """Calculate line total before saving."""
        price_after_discount = self.unit_price * (1 - self.discount_percent / 100)
        self.line_total = self.quantity_ordered * price_after_discount * (1 + self.tax_rate / 100)
        super().save(*args, **kwargs)
    
    @property
    def quantity_pending(self):
        """Calculate quantity yet to be received."""
        return self.quantity_ordered - self.quantity_received


class GoodsReceipt(models.Model):
    """
    Goods Receipt Note (GRN) - Records receipt of goods from supplier.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('received', 'Received'),
        ('inspected', 'Quality Inspected'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('partial', 'Partially Accepted'),
    ]
    
    # Basic Information
    grn_number = models.CharField(max_length=50, unique=True, verbose_name='GRN Number')
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.PROTECT, related_name='goods_receipts')
    
    # Receipt Information
    receipt_date = models.DateField()
    received_by = models.CharField(max_length=100)
    
    # Delivery Information
    delivery_note_number = models.CharField(max_length=100, blank=True, help_text='Supplier delivery note number')
    vehicle_number = models.CharField(max_length=50, blank=True)
    driver_name = models.CharField(max_length=100, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Quality Inspection
    inspected_by = models.CharField(max_length=100, blank=True)
    inspection_date = models.DateField(blank=True, null=True)
    inspection_notes = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-receipt_date', '-created_at']
        verbose_name = 'Goods Receipt Note'
        verbose_name_plural = 'Goods Receipt Notes'
    
    def __str__(self):
        return f"{self.grn_number} - PO: {self.purchase_order.po_number}"
    
    def get_absolute_url(self):
        return reverse('purchasing:goods_receipt_detail', kwargs={'pk': self.pk})


class GoodsReceiptItem(models.Model):
    """
    Line items for Goods Receipt Notes.
    """
    CONDITION_CHOICES = [
        ('good', 'Good'),
        ('damaged', 'Damaged'),
        ('defective', 'Defective'),
        ('expired', 'Expired'),
    ]
    
    goods_receipt = models.ForeignKey(GoodsReceipt, on_delete=models.CASCADE, related_name='items')
    po_item = models.ForeignKey(PurchaseOrderItem, on_delete=models.PROTECT)
    
    # Receipt Details
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity_accepted = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity_rejected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Condition
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Storage Location
    storage_location = models.CharField(max_length=100, blank=True)
    batch_number = models.CharField(max_length=100, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Goods Receipt Item'
        verbose_name_plural = 'Goods Receipt Items'
    
    def __str__(self):
        return f"{self.goods_receipt.grn_number} - {self.po_item.description[:50]}"


class RFQ(models.Model):
    """
    Request for Quotation - Request sent to suppliers for pricing.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent to Suppliers'),
        ('received', 'Quotations Received'),
        ('evaluated', 'Evaluated'),
        ('awarded', 'Awarded'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic Information
    rfq_number = models.CharField(max_length=50, unique=True, verbose_name='RFQ Number')
    title = models.CharField(max_length=200)
    
    # Reference
    requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Dates
    rfq_date = models.DateField(verbose_name='RFQ Date')
    submission_deadline = models.DateField(help_text='Deadline for supplier submissions')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Description
    description = models.TextField()
    
    # Terms
    terms_conditions = models.TextField(blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Created By
    created_by = models.CharField(max_length=100)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rfq_date', '-created_at']
        verbose_name = 'Request for Quotation (RFQ)'
        verbose_name_plural = 'Requests for Quotation (RFQs)'
    
    def __str__(self):
        return f"{self.rfq_number} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('purchasing:rfq_detail', kwargs={'pk': self.pk})


class RFQItem(models.Model):
    """
    Line items for RFQ.
    """
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='items')
    item_number = models.IntegerField(default=1)
    
    # Item Details
    description = models.CharField(max_length=500)
    specification = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit_of_measure = models.CharField(max_length=50, default='pcs')
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['item_number']
        verbose_name = 'RFQ Item'
        verbose_name_plural = 'RFQ Items'
    
    def __str__(self):
        return f"{self.rfq.rfq_number} - Item {self.item_number}"


class SupplierQuotation(models.Model):
    """
    Quotations received from suppliers in response to RFQ.
    """
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic Information
    quotation_number = models.CharField(max_length=50)
    rfq = models.ForeignKey(RFQ, on_delete=models.CASCADE, related_name='quotations')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='quotations')
    
    # Dates
    quotation_date = models.DateField()
    valid_until = models.DateField()
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    
    # Financial
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Terms
    payment_terms = models.CharField(max_length=200)
    delivery_time = models.CharField(max_length=100, help_text='Estimated delivery time')
    
    # Notes
    notes = models.TextField(blank=True)
    evaluation_notes = models.TextField(blank=True, help_text='Internal evaluation notes')
    
    # Score
    evaluation_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text='Evaluation score out of 100')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-quotation_date']
        unique_together = ['rfq', 'supplier']
        verbose_name = 'Supplier Quotation'
        verbose_name_plural = 'Supplier Quotations'
    
    def __str__(self):
        return f"{self.quotation_number} - {self.supplier.name}"
