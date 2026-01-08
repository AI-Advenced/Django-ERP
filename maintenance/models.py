"""
Maintenance & Asset Management Models
- Asset/Equipment: Equipment and assets tracking
- PreventiveMaintenance: Scheduled maintenance plans
- WorkOrder: Maintenance work orders
- MaintenanceLog: Maintenance history and logs
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.urls import reverse
from decimal import Decimal
from datetime import timedelta


class AssetCategory(models.Model):
    """Categories for assets and equipment"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Asset Category'
        verbose_name_plural = 'Asset Categories'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Asset(models.Model):
    """Equipment and Assets"""
    
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('repair', 'Under Repair'),
        ('idle', 'Idle'),
        ('retired', 'Retired'),
        ('disposed', 'Disposed'),
    ]
    
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    
    # Identification
    asset_number = models.CharField(max_length=50, unique=True, editable=False)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(AssetCategory, on_delete=models.PROTECT,
                                 related_name='assets')
    description = models.TextField()
    
    # Specifications
    manufacturer = models.CharField(max_length=200, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, blank=True, unique=True)
    year_manufactured = models.IntegerField(null=True, blank=True)
    
    # Location and Assignment
    location = models.CharField(max_length=200,
                               help_text="Physical location of the asset")
    department = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_assets')
    
    # Financial Information
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                           help_text="Annual depreciation rate (%)")
    
    # Status and Condition
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='operational')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    
    # Warranty and Service
    warranty_expiry = models.DateField(null=True, blank=True)
    service_contract_number = models.CharField(max_length=100, blank=True)
    service_provider = models.CharField(max_length=200, blank=True)
    
    # Maintenance Information
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    maintenance_interval_days = models.IntegerField(null=True, blank=True,
                                                    help_text="Days between maintenance")
    
    # Operational Metrics
    operating_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                         help_text="Total operating hours")
    downtime_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        help_text="Total downtime hours")
    
    # Documentation
    specifications = models.TextField(blank=True,
                                     help_text="Technical specifications")
    notes = models.TextField(blank=True)
    attachments = models.TextField(blank=True,
                                  help_text="File paths or URLs, comma-separated")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='assets_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Asset'
        verbose_name_plural = 'Assets'
        permissions = [
            ('can_retire_asset', 'Can retire asset'),
            ('can_dispose_asset', 'Can dispose asset'),
        ]
    
    def __str__(self):
        return f"{self.asset_number} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.asset_number:
            # Generate asset number
            last_asset = Asset.objects.order_by('-id').first()
            if last_asset and last_asset.asset_number:
                try:
                    last_number = int(last_asset.asset_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.asset_number = f"AST-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('maintenance:asset_detail', kwargs={'pk': self.pk})
    
    @property
    def is_warranty_valid(self):
        """Check if warranty is still valid"""
        from django.utils import timezone
        if self.warranty_expiry:
            return timezone.now().date() <= self.warranty_expiry
        return False
    
    @property
    def is_maintenance_due(self):
        """Check if maintenance is due"""
        from django.utils import timezone
        if self.next_maintenance_date:
            return timezone.now().date() >= self.next_maintenance_date
        return False
    
    @property
    def availability_rate(self):
        """Calculate asset availability rate"""
        total_hours = float(self.operating_hours) + float(self.downtime_hours)
        if total_hours > 0:
            return (float(self.operating_hours) / total_hours) * 100
        return 100.0
    
    @property
    def age_years(self):
        """Calculate asset age in years"""
        from django.utils import timezone
        if self.purchase_date:
            age_days = (timezone.now().date() - self.purchase_date).days
            return age_days / 365.25
        return None


class PreventiveMaintenance(models.Model):
    """Preventive Maintenance Plans"""
    
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('biweekly', 'Bi-Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('semiannual', 'Semi-Annual'),
        ('annual', 'Annual'),
        ('custom', 'Custom Interval'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    
    # Identification
    pm_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=200)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,
                             related_name='preventive_maintenances')
    
    # Description
    description = models.TextField()
    procedure = models.TextField(help_text="Detailed maintenance procedure")
    
    # Scheduling
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    interval_days = models.IntegerField(null=True, blank=True,
                                       help_text="Custom interval in days")
    start_date = models.DateField()
    next_due_date = models.DateField()
    last_performed_date = models.DateField(null=True, blank=True)
    
    # Assignment
    assigned_technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='pm_assignments')
    estimated_duration_hours = models.DecimalField(max_digits=5, decimal_places=2,
                                                   help_text="Estimated time in hours")
    
    # Resources
    required_parts = models.TextField(blank=True,
                                     help_text="List of required parts/materials")
    required_tools = models.TextField(blank=True,
                                     help_text="List of required tools")
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Checklist
    checklist = models.TextField(blank=True,
                                help_text="Maintenance checklist items, one per line")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_critical = models.BooleanField(default=False,
                                     help_text="Critical maintenance task")
    
    # Notifications
    notify_days_before = models.IntegerField(default=7,
                                            help_text="Days before to send notification")
    notification_emails = models.TextField(blank=True,
                                          help_text="Email addresses, comma-separated")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='pm_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['next_due_date']
        verbose_name = 'Preventive Maintenance'
        verbose_name_plural = 'Preventive Maintenances'
    
    def __str__(self):
        return f"{self.pm_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.pm_number:
            # Generate PM number
            last_pm = PreventiveMaintenance.objects.order_by('-id').first()
            if last_pm and last_pm.pm_number:
                try:
                    last_number = int(last_pm.pm_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.pm_number = f"PM-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('maintenance:pm_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        """Check if PM is overdue"""
        from django.utils import timezone
        if self.status == 'active':
            return timezone.now().date() > self.next_due_date
        return False
    
    @property
    def days_until_due(self):
        """Days until next maintenance"""
        from django.utils import timezone
        if self.status == 'active':
            delta = self.next_due_date - timezone.now().date()
            return delta.days
        return None
    
    def calculate_next_due_date(self):
        """Calculate next due date based on frequency"""
        from datetime import timedelta
        
        if self.frequency == 'daily':
            return self.last_performed_date + timedelta(days=1)
        elif self.frequency == 'weekly':
            return self.last_performed_date + timedelta(weeks=1)
        elif self.frequency == 'biweekly':
            return self.last_performed_date + timedelta(weeks=2)
        elif self.frequency == 'monthly':
            return self.last_performed_date + timedelta(days=30)
        elif self.frequency == 'quarterly':
            return self.last_performed_date + timedelta(days=90)
        elif self.frequency == 'semiannual':
            return self.last_performed_date + timedelta(days=180)
        elif self.frequency == 'annual':
            return self.last_performed_date + timedelta(days=365)
        elif self.frequency == 'custom' and self.interval_days:
            return self.last_performed_date + timedelta(days=self.interval_days)
        return self.next_due_date


class WorkOrder(models.Model):
    """Maintenance Work Orders"""
    
    TYPE_CHOICES = [
        ('corrective', 'Corrective Maintenance'),
        ('preventive', 'Preventive Maintenance'),
        ('inspection', 'Inspection'),
        ('repair', 'Repair'),
        ('installation', 'Installation'),
        ('emergency', 'Emergency'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]
    
    # Identification
    wo_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=200)
    work_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Asset and PM Link
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT,
                             related_name='work_orders')
    preventive_maintenance = models.ForeignKey(PreventiveMaintenance, on_delete=models.SET_NULL,
                                              null=True, blank=True,
                                              related_name='work_orders')
    
    # Description
    description = models.TextField()
    problem_reported = models.TextField(blank=True,
                                       help_text="Problem description")
    root_cause = models.TextField(blank=True,
                                  help_text="Root cause analysis")
    resolution = models.TextField(blank=True,
                                 help_text="Resolution details")
    
    # Priority and Status
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Assignment
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='assigned_work_orders')
    assigned_team = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                          related_name='team_work_orders')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='supervised_work_orders')
    
    # Scheduling
    requested_date = models.DateField()
    scheduled_start = models.DateTimeField(null=True, blank=True)
    scheduled_end = models.DateTimeField(null=True, blank=True)
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Costs
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    parts_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Parts and Materials
    parts_used = models.TextField(blank=True,
                                 help_text="Parts used, one per line")
    tools_used = models.TextField(blank=True,
                                 help_text="Tools used")
    
    # Approval
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='wo_approved')
    approval_date = models.DateField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Completion
    completion_notes = models.TextField(blank=True)
    verification_required = models.BooleanField(default=False)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='wo_verified')
    verification_date = models.DateField(null=True, blank=True)
    
    # Safety
    safety_precautions = models.TextField(blank=True)
    lockout_tagout_required = models.BooleanField(default=False)
    permit_required = models.BooleanField(default=False)
    permit_number = models.CharField(max_length=100, blank=True)
    
    # Attachments
    attachments = models.TextField(blank=True,
                                  help_text="File paths or URLs, comma-separated")
    
    # Tracking
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='wo_requested')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='wo_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Work Order'
        verbose_name_plural = 'Work Orders'
        permissions = [
            ('can_approve_work_order', 'Can approve work order'),
            ('can_close_work_order', 'Can close work order'),
        ]
    
    def __str__(self):
        return f"{self.wo_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.wo_number:
            # Generate WO number
            last_wo = WorkOrder.objects.order_by('-id').first()
            if last_wo and last_wo.wo_number:
                try:
                    last_number = int(last_wo.wo_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.wo_number = f"WO-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('maintenance:workorder_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        """Check if work order is overdue"""
        from django.utils import timezone
        if self.status not in ['completed', 'closed', 'cancelled']:
            if self.scheduled_end:
                return timezone.now() > self.scheduled_end
        return False
    
    @property
    def duration_hours(self):
        """Calculate actual duration in hours"""
        if self.actual_start and self.actual_end:
            delta = self.actual_end - self.actual_start
            return delta.total_seconds() / 3600
        return None
    
    @property
    def total_cost(self):
        """Calculate total cost"""
        return float(self.labor_cost) + float(self.parts_cost) + float(self.other_cost)


class MaintenanceLog(models.Model):
    """Maintenance History and Logs"""
    
    LOG_TYPE_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection'),
        ('breakdown', 'Breakdown'),
        ('note', 'Note'),
    ]
    
    # References
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE,
                             related_name='maintenance_logs')
    work_order = models.ForeignKey(WorkOrder, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='logs')
    
    # Log Details
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Work Done
    work_performed = models.TextField(blank=True)
    parts_replaced = models.TextField(blank=True)
    technician = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='maintenance_logs')
    
    # Metrics
    hours_spent = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Status
    downtime_start = models.DateTimeField(null=True, blank=True)
    downtime_end = models.DateTimeField(null=True, blank=True)
    asset_operational = models.BooleanField(default=True,
                                           help_text="Is asset operational after maintenance?")
    
    # Notes
    notes = models.TextField(blank=True)
    recommendations = models.TextField(blank=True,
                                      help_text="Recommendations for future maintenance")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='logs_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        verbose_name = 'Maintenance Log'
        verbose_name_plural = 'Maintenance Logs'
    
    def __str__(self):
        return f"{self.asset.asset_number} - {self.title} ({self.date})"
    
    @property
    def downtime_duration(self):
        """Calculate downtime duration in hours"""
        if self.downtime_start and self.downtime_end:
            delta = self.downtime_end - self.downtime_start
            return delta.total_seconds() / 3600
        return 0
