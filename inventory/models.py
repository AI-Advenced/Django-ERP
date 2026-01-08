from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Product Category"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
    
    def get_absolute_url(self):
        return reverse('inventory:category_detail', kwargs={'pk': self.pk})

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name
        
class Unit(models.Model):
    """Unit of Measurement"""
    name = models.CharField(max_length=50, unique=True)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Unit of Measurement'
        verbose_name_plural = 'Units of Measurement'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Product(models.Model):
    """Product/Item Model"""
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Pricing
    cost_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        help_text='Purchase/cost price'
    )
    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        help_text='Selling price'
    )
    
    # Stock Management
    track_inventory = models.BooleanField(default=True)
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    minimum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        help_text='Minimum stock level for alerts'
    )
    maximum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00'),
        blank=True,
        help_text='Maximum stock level'
    )
    
    # Additional Info
    barcode = models.CharField(max_length=100, blank=True, null=True, unique=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_products'
    )
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('inventory:product_detail', kwargs={'pk': self.pk})
    
    def is_low_stock(self):
        """Check if product is below minimum stock"""
        if self.track_inventory and self.minimum_stock > 0:
            return self.current_stock <= self.minimum_stock
        return False
    
    def stock_status(self):
        """Return stock status"""
        if not self.track_inventory:
            return 'Not Tracked'
        if self.current_stock <= 0:
            return 'Out of Stock'
        elif self.is_low_stock():
            return 'Low Stock'
        return 'In Stock'
    
    def profit_margin(self):
        """Calculate profit margin"""
        if self.cost_price > 0:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0


class Location(models.Model):
    """Storage Location/Warehouse"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Storage Location'
        verbose_name_plural = 'Storage Locations'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('inventory:location_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Ensure only one default location
        if self.is_default:
            Location.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)


class StockMovement(models.Model):
    """Stock Movement/Transaction"""
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
    ]
    
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPE_CHOICES)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Location
    location_from = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movements_from'
    )
    location_to = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movements_to'
    )
    
    # Details
    reference = models.CharField(max_length=100, blank=True, null=True, help_text='PO number, invoice, etc.')
    notes = models.TextField(blank=True, null=True)
    unit_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    
    # Stock levels after movement
    stock_before = models.DecimalField(max_digits=12, decimal_places=2)
    stock_after = models.DecimalField(max_digits=12, decimal_places=2)
    
    # User and timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='stock_movements'
    )
    
    class Meta:
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.code} - {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('inventory:movement_detail', kwargs={'pk': self.pk})
    
    def total_cost(self):
        """Calculate total cost of movement"""
        return self.quantity * self.unit_cost
    
    def save(self, *args, **kwargs):
        # Record stock before
        self.stock_before = self.product.current_stock
        
        # Update product stock
        if self.movement_type == 'in':
            self.product.current_stock += self.quantity
        elif self.movement_type == 'out':
            self.product.current_stock -= self.quantity
            if self.product.current_stock < 0:
                self.product.current_stock = Decimal('0.00')
        elif self.movement_type == 'adjustment':
            # Adjustment can be positive or negative
            # quantity field stores the new stock level for adjustments
            self.product.current_stock = self.quantity
        
        # Record stock after
        self.stock_after = self.product.current_stock
        self.product.save()
        
        super().save(*args, **kwargs)


class ProductLocation(models.Model):
    """Product Stock at Specific Location"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='location_stock'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='product_stock'
    )
    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        default=Decimal('0.00')
    )
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Product Location Stock'
        verbose_name_plural = 'Product Location Stock'
        unique_together = ['product', 'location']
        ordering = ['product__name']
    
    def __str__(self):
        return f"{self.product.code} at {self.location.code}: {self.quantity}"
