from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Customer(models.Model):
    """
    Sales Customer Model
    """
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('government', 'Government'),
    ]

    # Basic Information
    name = models.CharField(max_length=200)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20, blank=True)
    
    # Address Information
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='USA')
    postal_code = models.CharField(max_length=20)
    
    # Business Information
    company_name = models.CharField(max_length=200, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, help_text="Tax ID/VAT Number")
    website = models.URLField(blank=True)
    
    # Financial
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_terms = models.IntegerField(default=30, help_text="Payment terms in days")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return f"{self.name} ({self.customer_type})"

    def get_absolute_url(self):
        return reverse('sales:customer_detail', kwargs={'pk': self.pk})

    @property
    def total_orders_value(self):
        """Calculate total value of all orders"""
        return self.sales_orders.aggregate(
            total=models.Sum('total_amount')
        )['total'] or Decimal('0.00')

    @property
    def outstanding_balance(self):
        """Calculate outstanding balance"""
        return self.sales_orders.filter(
            status__in=['confirmed', 'delivered']
        ).aggregate(
            total=models.Sum('total_amount') - models.Sum('paid_amount')
        )['total'] or Decimal('0.00')


class SalesOrder(models.Model):
    """
    Sales Order Model
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('quotation', 'Quotation'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
        ('invoiced', 'Invoiced'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    # Order Information
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='sales_orders')
    order_date = models.DateField()
    expected_delivery_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    
    # Financial Details
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, 
                                   help_text="Tax rate in percentage")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Shipping Information
    shipping_address = models.TextField(blank=True)
    shipping_city = models.CharField(max_length=100, blank=True)
    shipping_state = models.CharField(max_length=100, blank=True)
    shipping_country = models.CharField(max_length=100, blank=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True)
    
    # Additional Information
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True, help_text="Internal notes (not visible to customer)")
    
    # Sales Person (optional - can be linked to User model)
    sales_person = models.CharField(max_length=200, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_date = models.DateTimeField(blank=True, null=True)
    delivered_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-order_date', '-order_number']
        verbose_name = 'Sales Order'
        verbose_name_plural = 'Sales Orders'

    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"

    def get_absolute_url(self):
        return reverse('sales:order_detail', kwargs={'pk': self.pk})

    @property
    def balance_due(self):
        """Calculate balance due"""
        return self.total_amount - self.paid_amount

    @property
    def is_paid(self):
        """Check if order is fully paid"""
        return self.paid_amount >= self.total_amount

    def calculate_totals(self):
        """Calculate order totals"""
        # Calculate subtotal from items
        items_total = self.items.aggregate(
            total=models.Sum(models.F('quantity') * models.F('unit_price'))
        )['total'] or Decimal('0.00')
        
        self.subtotal = items_total
        
        # Calculate discount
        if self.discount_percentage > 0:
            self.discount_amount = (self.subtotal * self.discount_percentage / 100)
        
        # Calculate tax
        taxable_amount = self.subtotal - self.discount_amount
        if self.tax_rate > 0:
            self.tax_amount = (taxable_amount * self.tax_rate / 100)
        
        # Calculate total
        self.total_amount = taxable_amount + self.tax_amount + self.shipping_cost
        
        return self.total_amount


class SalesOrderItem(models.Model):
    """
    Sales Order Line Items
    """
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=500)
    product_code = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1,
                                   validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Sales Order Item'
        verbose_name_plural = 'Sales Order Items'

    def __str__(self):
        return f"{self.product_name} - {self.quantity} x ${self.unit_price}"

    @property
    def line_total(self):
        """Calculate line total"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_percentage / 100)
        after_discount = subtotal - discount
        tax = after_discount * (self.tax_rate / 100)
        return after_discount + tax


class Quotation(models.Model):
    """
    Sales Quotation/Quote Model
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('converted', 'Converted to Order'),
    ]

    # Quotation Information
    quotation_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='quotations')
    quotation_date = models.DateField()
    valid_until = models.DateField(help_text="Quote validity date")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Financial Details
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Additional Information
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    # Conversion
    converted_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, 
                                       blank=True, null=True, related_name='source_quotation')
    
    # Sales Person
    sales_person = models.CharField(max_length=200, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-quotation_date', '-quotation_number']
        verbose_name = 'Quotation'
        verbose_name_plural = 'Quotations'

    def __str__(self):
        return f"{self.quotation_number} - {self.customer.name}"

    def get_absolute_url(self):
        return reverse('sales:quotation_detail', kwargs={'pk': self.pk})

    @property
    def is_valid(self):
        """Check if quotation is still valid"""
        from django.utils import timezone
        return timezone.now().date() <= self.valid_until

    def calculate_totals(self):
        """Calculate quotation totals"""
        items_total = self.items.aggregate(
            total=models.Sum(models.F('quantity') * models.F('unit_price'))
        )['total'] or Decimal('0.00')
        
        self.subtotal = items_total
        taxable_amount = self.subtotal - self.discount_amount
        
        if self.tax_rate > 0:
            self.tax_amount = (taxable_amount * self.tax_rate / 100)
        
        self.total_amount = taxable_amount + self.tax_amount
        return self.total_amount


class QuotationItem(models.Model):
    """
    Quotation Line Items
    """
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=500)
    product_code = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1,
                                   validators=[MinValueValidator(0.01)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Quotation Item'
        verbose_name_plural = 'Quotation Items'

    def __str__(self):
        return f"{self.product_name} - {self.quantity} x ${self.unit_price}"

    @property
    def line_total(self):
        """Calculate line total"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_percentage / 100)
        return subtotal - discount
