from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal

User = get_user_model()


class Account(models.Model):
    """
    Chart of Accounts - Accounts for financial transactions
    """
    ACCOUNT_TYPES = [
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('revenue', 'Revenue'),
        ('expense', 'Expense'),
    ]
    
    code = models.CharField(max_length=20, unique=True, help_text="Account code (e.g., 1000, 2000)")
    name = models.CharField(max_length=200)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('financial:account_detail', kwargs={'pk': self.pk})
    
    def get_balance(self):
        """Calculate current account balance"""
        debits = self.journal_entries_debit.aggregate(
            total=models.Sum('debit_amount'))['total'] or Decimal('0.00')
        credits = self.journal_entries_credit.aggregate(
            total=models.Sum('credit_amount'))['total'] or Decimal('0.00')
        
        if self.account_type in ['asset', 'expense']:
            return debits - credits
        else:  # liability, equity, revenue
            return credits - debits


class Customer(models.Model):
    """
    Customer/Client for invoicing
    """
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    tax_id = models.CharField(max_length=50, blank=True, help_text="Tax ID or VAT number")
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('financial:customer_detail', kwargs={'pk': self.pk})
    
    def get_total_invoices(self):
        return self.invoices.aggregate(total=models.Sum('total_amount'))['total'] or Decimal('0.00')
    
    def get_outstanding_balance(self):
        return self.invoices.filter(status__in=['draft', 'sent', 'overdue']).aggregate(
            total=models.Sum('total_amount'))['total'] or Decimal('0.00')


class Invoice(models.Model):
    """
    Sales Invoice
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    invoice_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    invoice_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Tax rate in percentage")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Additional info
    notes = models.TextField(blank=True)
    terms = models.TextField(blank=True, help_text="Payment terms and conditions")
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-invoice_date', '-invoice_number']
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'
    
    def __str__(self):
        return f"{self.invoice_number} - {self.customer.name}"
    
    def get_absolute_url(self):
        return reverse('financial:invoice_detail', kwargs={'pk': self.pk})
    
    def calculate_totals(self):
        """Calculate invoice totals"""
        self.subtotal = sum(item.total_price for item in self.items.all())
        self.tax_amount = (self.subtotal * self.tax_rate) / Decimal('100.00')
        self.total_amount = self.subtotal + self.tax_amount - self.discount_amount
        self.save()
    
    def get_balance_due(self):
        return self.total_amount - self.paid_amount


class InvoiceItem(models.Model):
    """
    Invoice line items
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Invoice Item'
        verbose_name_plural = 'Invoice Items'
    
    def __str__(self):
        return f"{self.description} - {self.quantity} x {self.unit_price}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Bill(models.Model):
    """
    Purchase Bill / Vendor Invoice
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    bill_number = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=200)
    vendor_email = models.EmailField(blank=True)
    vendor_phone = models.CharField(max_length=20, blank=True)
    
    bill_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_bills')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-bill_date', '-bill_number']
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'
    
    def __str__(self):
        return f"{self.bill_number} - {self.vendor_name}"
    
    def get_absolute_url(self):
        return reverse('financial:bill_detail', kwargs={'pk': self.pk})
    
    def get_balance_due(self):
        return self.total_amount - self.paid_amount


class Payment(models.Model):
    """
    Payment transactions (both received and made)
    """
    PAYMENT_TYPES = [
        ('received', 'Payment Received'),
        ('made', 'Payment Made'),
    ]
    
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    ]
    
    payment_number = models.CharField(max_length=50, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    
    # Related documents
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    bill = models.ForeignKey(Bill, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    
    reference_number = models.CharField(max_length=100, blank=True, help_text="Check number, transaction ID, etc.")
    notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date', '-payment_number']
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
    
    def __str__(self):
        return f"{self.payment_number} - {self.get_payment_type_display()} - ${self.amount}"
    
    def get_absolute_url(self):
        return reverse('financial:payment_detail', kwargs={'pk': self.pk})


class JournalEntry(models.Model):
    """
    General Journal Entries for double-entry bookkeeping
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('void', 'Void'),
    ]
    
    entry_number = models.CharField(max_length=50, unique=True)
    entry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    description = models.CharField(max_length=500)
    notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_entries')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-entry_date', '-entry_number']
        verbose_name = 'Journal Entry'
        verbose_name_plural = 'Journal Entries'
    
    def __str__(self):
        return f"{self.entry_number} - {self.description}"
    
    def get_absolute_url(self):
        return reverse('financial:journal_entry_detail', kwargs={'pk': self.pk})
    
    def get_total_debit(self):
        return self.lines.aggregate(total=models.Sum('debit_amount'))['total'] or Decimal('0.00')
    
    def get_total_credit(self):
        return self.lines.aggregate(total=models.Sum('credit_amount'))['total'] or Decimal('0.00')
    
    def is_balanced(self):
        return self.get_total_debit() == self.get_total_credit()


class JournalEntryLine(models.Model):
    """
    Journal Entry Lines (debit and credit entries)
    """
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='journal_entries')
    debit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Journal Entry Line'
        verbose_name_plural = 'Journal Entry Lines'
    
    def __str__(self):
        return f"{self.account.code} - Debit: {self.debit_amount} Credit: {self.credit_amount}"


class Expense(models.Model):
    """
    Business Expenses
    """
    EXPENSE_CATEGORIES = [
        ('rent', 'Rent'),
        ('utilities', 'Utilities'),
        ('salaries', 'Salaries'),
        ('marketing', 'Marketing'),
        ('office_supplies', 'Office Supplies'),
        ('travel', 'Travel'),
        ('meals', 'Meals & Entertainment'),
        ('insurance', 'Insurance'),
        ('maintenance', 'Maintenance'),
        ('other', 'Other'),
    ]
    
    expense_number = models.CharField(max_length=50, unique=True)
    expense_date = models.DateField()
    category = models.CharField(max_length=50, choices=EXPENSE_CATEGORIES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    vendor_name = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500)
    payment_method = models.CharField(max_length=20, choices=Payment.PAYMENT_METHODS, default='cash')
    receipt_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    is_billable = models.BooleanField(default=False, help_text="Can be billed to customer")
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-expense_date', '-expense_number']
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
    
    def __str__(self):
        return f"{self.expense_number} - {self.get_category_display()} - ${self.amount}"
    
    def get_absolute_url(self):
        return reverse('financial:expense_detail', kwargs={'pk': self.pk})


class Budget(models.Model):
    """
    Budget planning and tracking
    """
    PERIOD_TYPES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=200)
    period_type = models.CharField(max_length=20, choices=PERIOD_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='budgets')
    budgeted_amount = models.DecimalField(max_digits=12, decimal_places=2)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_budgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
    
    def __str__(self):
        return f"{self.name} - {self.start_date} to {self.end_date}"
    
    def get_absolute_url(self):
        return reverse('financial:budget_detail', kwargs={'pk': self.pk})
    
    def get_variance(self):
        return self.budgeted_amount - self.actual_amount
    
    def get_variance_percentage(self):
        if self.budgeted_amount > 0:
            return ((self.actual_amount - self.budgeted_amount) / self.budgeted_amount) * Decimal('100.00')
        return Decimal('0.00')
