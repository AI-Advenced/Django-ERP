from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal

User = get_user_model()


class TaxRate(models.Model):
    """Tax Rate Configuration"""
    TAX_TYPE_CHOICES = [
        ('vat', 'VAT (Value Added Tax)'),
        ('sales', 'Sales Tax'),
        ('income', 'Income Tax'),
        ('corporate', 'Corporate Tax'),
        ('withholding', 'Withholding Tax'),
        ('customs', 'Customs Duty'),
        ('excise', 'Excise Tax'),
    ]
    
    name = models.CharField(max_length=100)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tax rate in percentage")
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, default='USA')
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tax Rate'
        verbose_name_plural = 'Tax Rates'
    
    def __str__(self):
        return f"{self.name} ({self.rate}%)"
    
    def get_absolute_url(self):
        return reverse('fiscal:taxrate_detail', kwargs={'pk': self.pk})


class FiscalYear(models.Model):
    """Fiscal Year Configuration"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ]
    
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fiscal_years_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Fiscal Year'
        verbose_name_plural = 'Fiscal Years'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('fiscal:fiscalyear_detail', kwargs={'pk': self.pk})


class Invoice(models.Model):
    """Invoice Management"""
    INVOICE_TYPE_CHOICES = [
        ('sales', 'Sales Invoice'),
        ('purchase', 'Purchase Invoice'),
        ('proforma', 'Proforma Invoice'),
        ('credit_note', 'Credit Note'),
        ('debit_note', 'Debit Note'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    invoice_type = models.CharField(max_length=20, choices=INVOICE_TYPE_CHOICES)
    invoice_date = models.DateField()
    due_date = models.DateField()
    
    # Customer/Vendor Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True)
    customer_address = models.TextField(blank=True)
    customer_tax_id = models.CharField(max_length=50, blank=True)
    
    # Financial Details
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status and Additional Info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    # Fiscal Information
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='invoices_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date', '-invoice_number']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer_name}"
    
    def get_absolute_url(self):
        return reverse('fiscal:invoice_detail', kwargs={'pk': self.pk})
    
    def calculate_balance(self):
        """Calculate remaining balance"""
        return self.total_amount - self.paid_amount
    
    def save(self, *args, **kwargs):
        self.balance = self.calculate_balance()
        super().save(*args, **kwargs)


class InvoiceItem(models.Model):
    """Invoice Line Items"""
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    tax_rate = models.ForeignKey(TaxRate, on_delete=models.SET_NULL, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description}"
    
    def calculate_line_total(self):
        """Calculate line total with tax and discount"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_percent / 100)
        subtotal_after_discount = subtotal - discount
        
        if self.tax_rate:
            tax = subtotal_after_discount * (self.tax_rate.rate / 100)
            return subtotal_after_discount + tax
        return subtotal_after_discount
    
    def save(self, *args, **kwargs):
        self.line_total = self.calculate_line_total()
        super().save(*args, **kwargs)


class Payment(models.Model):
    """Payment Records"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    payment_number = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    reference_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"{self.payment_number} - ${self.amount}"
    
    def get_absolute_url(self):
        return reverse('fiscal:payment_detail', kwargs={'pk': self.pk})


class TaxReport(models.Model):
    """Tax Report Generation"""
    REPORT_TYPE_CHOICES = [
        ('vat_return', 'VAT Return'),
        ('sales_tax', 'Sales Tax Report'),
        ('income_tax', 'Income Tax Report'),
        ('quarterly', 'Quarterly Tax Report'),
        ('annual', 'Annual Tax Report'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    report_number = models.CharField(max_length=50, unique=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_purchases = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_collected = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tax_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    net_tax = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    submitted_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-period_end']
        verbose_name = 'Tax Report'
        verbose_name_plural = 'Tax Reports'
    
    def __str__(self):
        return f"{self.report_number} - {self.report_type}"
    
    def get_absolute_url(self):
        return reverse('fiscal:taxreport_detail', kwargs={'pk': self.pk})
    
    def calculate_net_tax(self):
        """Calculate net tax (tax collected - tax paid)"""
        return self.tax_collected - self.tax_paid
    
    def save(self, *args, **kwargs):
        self.net_tax = self.calculate_net_tax()
        super().save(*args, **kwargs)
