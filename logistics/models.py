"""
Models for Logistics & Supply Chain Management Module
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal


class Warehouse(models.Model):
    """Warehouse/Storage Location model"""
    WAREHOUSE_TYPES = [
        ('main', 'Main Warehouse'),
        ('regional', 'Regional Warehouse'),
        ('distribution', 'Distribution Center'),
        ('retail', 'Retail Store'),
        ('virtual', 'Virtual Warehouse'),
    ]

    code = models.CharField(max_length=50, unique=True, help_text="Unique warehouse code")
    name = models.CharField(max_length=200, help_text="Warehouse name")
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES, default='main')
    
    # Location details
    address = models.TextField(help_text="Physical address")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Capacity
    total_capacity = models.DecimalField(max_digits=15, decimal_places=2, 
                                        validators=[MinValueValidator(0)],
                                        help_text="Total capacity in cubic meters")
    current_utilization = models.DecimalField(max_digits=15, decimal_places=2, 
                                             default=0, validators=[MinValueValidator(0)])
    
    # Contact
    manager_name = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['code']
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_utilization_percentage(self):
        """Calculate utilization percentage"""
        if self.total_capacity > 0:
            return (self.current_utilization / self.total_capacity) * 100
        return 0


class Inventory(models.Model):
    """Inventory/Stock model"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_items')
    
    # Product details (simplified - in real app would link to Product model)
    product_code = models.CharField(max_length=100, help_text="Product SKU/Code")
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    # Stock levels
    quantity_on_hand = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                          validators=[MinValueValidator(0)])
    quantity_reserved = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                           validators=[MinValueValidator(0)])
    quantity_available = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                            validators=[MinValueValidator(0)])
    reorder_level = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                       validators=[MinValueValidator(0)])
    reorder_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                          validators=[MinValueValidator(0)])
    
    # Valuation
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                    validators=[MinValueValidator(0)])
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     validators=[MinValueValidator(0)])
    
    # Location within warehouse
    bin_location = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    last_count_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['warehouse', 'product_code']
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'
        unique_together = ['warehouse', 'product_code']

    def __str__(self):
        return f"{self.product_code} - {self.warehouse.code} ({self.quantity_on_hand})"

    def is_below_reorder_level(self):
        """Check if stock is below reorder level"""
        return self.quantity_available < self.reorder_level

    def update_totals(self):
        """Update calculated fields"""
        self.quantity_available = self.quantity_on_hand - self.quantity_reserved
        self.total_value = self.quantity_on_hand * self.unit_cost


class Shipment(models.Model):
    """Shipment tracking model"""
    SHIPMENT_TYPES = [
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('transfer', 'Internal Transfer'),
        ('return', 'Return'),
    ]

    SHIPMENT_STATUS = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('delayed', 'Delayed'),
    ]

    TRANSPORT_MODES = [
        ('air', 'Air Freight'),
        ('sea', 'Sea Freight'),
        ('road', 'Road Transport'),
        ('rail', 'Rail Transport'),
        ('courier', 'Courier Service'),
    ]

    # Basic info
    shipment_number = models.CharField(max_length=100, unique=True)
    shipment_type = models.CharField(max_length=20, choices=SHIPMENT_TYPES)
    status = models.CharField(max_length=20, choices=SHIPMENT_STATUS, default='pending')
    
    # Origin and destination
    origin_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, 
                                        null=True, related_name='outbound_shipments')
    destination_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, 
                                             null=True, related_name='inbound_shipments')
    
    # Shipping details
    carrier_name = models.CharField(max_length=200)
    transport_mode = models.CharField(max_length=20, choices=TRANSPORT_MODES)
    tracking_number = models.CharField(max_length=200, blank=True)
    
    # Dates
    scheduled_ship_date = models.DateField()
    actual_ship_date = models.DateField(null=True, blank=True)
    estimated_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    
    # Financial
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                       validators=[MinValueValidator(0)])
    insurance_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                        validators=[MinValueValidator(0)])
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                     validators=[MinValueValidator(0)])
    
    # Additional info
    notes = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    
    # Reference
    reference_document = models.CharField(max_length=200, blank=True,
                                         help_text="PO/SO/Transfer Order reference")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'

    def __str__(self):
        return f"{self.shipment_number} - {self.get_shipment_type_display()}"

    def is_delayed(self):
        """Check if shipment is delayed"""
        if self.status not in ['delivered', 'cancelled']:
            return timezone.now().date() > self.estimated_delivery_date
        return False


class ShipmentItem(models.Model):
    """Items in a shipment"""
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='items')
    
    # Product details
    product_code = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Quantities
    quantity_shipped = models.DecimalField(max_digits=15, decimal_places=2,
                                          validators=[MinValueValidator(0)])
    quantity_received = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                           validators=[MinValueValidator(0)])
    
    # Packaging
    unit_of_measure = models.CharField(max_length=50, default='PCS')
    package_count = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                validators=[MinValueValidator(0)], help_text="Weight in kg")
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                validators=[MinValueValidator(0)], help_text="Volume in cubic meters")
    
    # Valuation
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                    validators=[MinValueValidator(0)])
    line_total = models.DecimalField(max_digits=15, decimal_places=2, default=0,
                                    validators=[MinValueValidator(0)])
    
    # Inventory reference
    inventory = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Shipment Item'
        verbose_name_plural = 'Shipment Items'

    def __str__(self):
        return f"{self.product_code} - {self.quantity_shipped} {self.unit_of_measure}"

    def calculate_line_total(self):
        """Calculate line total"""
        self.line_total = self.quantity_shipped * self.unit_price


class Route(models.Model):
    """Delivery route model"""
    ROUTE_STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('planning', 'Planning'),
    ]

    route_code = models.CharField(max_length=50, unique=True)
    route_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=ROUTE_STATUS, default='planning')
    
    # Route details
    start_warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, 
                                       related_name='routes_starting')
    description = models.TextField(blank=True)
    
    # Metrics
    total_distance = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        validators=[MinValueValidator(0)], 
                                        help_text="Total distance in km")
    estimated_duration = models.DurationField(help_text="Estimated travel time")
    
    # Cost
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                        validators=[MinValueValidator(0)])
    
    # Schedule
    frequency = models.CharField(max_length=100, blank=True, 
                                help_text="e.g., Daily, Weekly, etc.")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['route_code']
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'

    def __str__(self):
        return f"{self.route_code} - {self.route_name}"


class Delivery(models.Model):
    """Delivery execution model"""
    DELIVERY_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    delivery_number = models.CharField(max_length=100, unique=True)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, blank=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='deliveries')
    
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='scheduled')
    
    # Delivery details
    delivery_address = models.TextField()
    delivery_contact = models.CharField(max_length=200)
    delivery_phone = models.CharField(max_length=50)
    
    # Schedule
    scheduled_date = models.DateTimeField()
    actual_start_time = models.DateTimeField(null=True, blank=True)
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    # Driver/Vehicle info
    driver_name = models.CharField(max_length=200, blank=True)
    vehicle_number = models.CharField(max_length=100, blank=True)
    
    # Proof of delivery
    signature = models.TextField(blank=True, help_text="Digital signature data")
    delivery_photo_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-scheduled_date']
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return f"{self.delivery_number} - {self.status}"

    def is_overdue(self):
        """Check if delivery is overdue"""
        if self.status in ['scheduled', 'in_progress']:
            return timezone.now() > self.scheduled_date
        return False


class StockMovement(models.Model):
    """Stock movement/transaction log"""
    MOVEMENT_TYPES = [
        ('receipt', 'Receipt'),
        ('issue', 'Issue'),
        ('adjustment', 'Adjustment'),
        ('transfer', 'Transfer'),
        ('return', 'Return'),
        ('scrap', 'Scrap'),
    ]

    movement_number = models.CharField(max_length=100, unique=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    movement_date = models.DateTimeField(default=timezone.now)
    
    # Inventory reference
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, 
                                 related_name='movements')
    
    # Quantity
    quantity = models.DecimalField(max_digits=15, decimal_places=2,
                                  help_text="Positive for increase, negative for decrease")
    unit_of_measure = models.CharField(max_length=50, default='PCS')
    
    # Cost
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                   validators=[MinValueValidator(0)])
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # References
    reference_document = models.CharField(max_length=200, blank=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Transfer info (if movement is a transfer)
    from_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, 
                                      blank=True, related_name='movements_from')
    to_warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, 
                                    blank=True, related_name='movements_to')
    
    # Additional info
    reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # User tracking (simplified - in real app would link to User model)
    created_by = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-movement_date']
        verbose_name = 'Stock Movement'
        verbose_name_plural = 'Stock Movements'

    def __str__(self):
        return f"{self.movement_number} - {self.get_movement_type_display()}"

    def calculate_total(self):
        """Calculate total cost"""
        self.total_cost = abs(self.quantity) * self.unit_cost
