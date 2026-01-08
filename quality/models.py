"""
Quality Management Models
- Inspection: Quality inspections with checkpoints
- NonConformance: Track quality issues and defects
- CorrectiveAction: Manage corrective and preventive actions
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from decimal import Decimal


class InspectionType(models.Model):
    """Types of quality inspections"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Inspection Type'
        verbose_name_plural = 'Inspection Types'
    
    def __str__(self):
        return f"{self.code} - {self.name}"


class Inspection(models.Model):
    """Quality Inspections"""
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    inspection_number = models.CharField(max_length=50, unique=True, editable=False)
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Reference Information
    reference_type = models.CharField(max_length=50, blank=True,
                                     help_text="e.g., Purchase Order, Production Batch, Sales Order")
    reference_number = models.CharField(max_length=100, blank=True)
    
    # Scheduling
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Assignment
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                 related_name='inspections_conducted')
    supervisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='inspections_supervised')
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Results
    overall_result = models.CharField(max_length=20, choices=[
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('conditional', 'Conditional Pass'),
    ], blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                               validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Notes and Attachments
    notes = models.TextField(blank=True)
    attachments = models.TextField(blank=True, help_text="File paths or URLs, comma-separated")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='inspections_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-scheduled_date', '-created_at']
        verbose_name = 'Inspection'
        verbose_name_plural = 'Inspections'
        permissions = [
            ('can_approve_inspection', 'Can approve inspection'),
            ('can_view_reports', 'Can view quality reports'),
        ]
    
    def __str__(self):
        return f"{self.inspection_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.inspection_number:
            # Generate inspection number
            last_inspection = Inspection.objects.order_by('-id').first()
            if last_inspection and last_inspection.inspection_number:
                try:
                    last_number = int(last_inspection.inspection_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.inspection_number = f"INSP-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('quality:inspection_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        """Check if inspection is overdue"""
        from django.utils import timezone
        if self.status in ['scheduled', 'in_progress']:
            return timezone.now().date() > self.scheduled_date
        return False
    
    @property
    def checkpoint_count(self):
        """Count of inspection checkpoints"""
        return self.checkpoints.count()
    
    @property
    def passed_checkpoints(self):
        """Count of passed checkpoints"""
        return self.checkpoints.filter(result='pass').count()


class InspectionCheckpoint(models.Model):
    """Individual checkpoints within an inspection"""
    
    RESULT_CHOICES = [
        ('pass', 'Pass'),
        ('fail', 'Fail'),
        ('na', 'Not Applicable'),
    ]
    
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE,
                                  related_name='checkpoints')
    sequence = models.IntegerField(default=0)
    checkpoint_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Criteria
    acceptance_criteria = models.TextField()
    measurement_method = models.CharField(max_length=200, blank=True)
    
    # Results
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, blank=True)
    measured_value = models.CharField(max_length=100, blank=True)
    observations = models.TextField(blank=True)
    
    # Tracking
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['inspection', 'sequence']
        verbose_name = 'Inspection Checkpoint'
        verbose_name_plural = 'Inspection Checkpoints'
    
    def __str__(self):
        return f"{self.inspection.inspection_number} - {self.checkpoint_name}"


class NonConformance(models.Model):
    """Non-Conformance Reports (NCR)"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('reported', 'Reported'),
        ('investigating', 'Under Investigation'),
        ('action_required', 'Action Required'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ]
    
    SEVERITY_CHOICES = [
        ('minor', 'Minor'),
        ('major', 'Major'),
        ('critical', 'Critical'),
    ]
    
    SOURCE_CHOICES = [
        ('inspection', 'Quality Inspection'),
        ('customer', 'Customer Complaint'),
        ('internal', 'Internal Audit'),
        ('supplier', 'Supplier Quality'),
        ('production', 'Production'),
        ('other', 'Other'),
    ]
    
    ncr_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Source and Reference
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    inspection = models.ForeignKey(Inspection, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='non_conformances')
    reference_type = models.CharField(max_length=50, blank=True)
    reference_number = models.CharField(max_length=100, blank=True)
    
    # Classification
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='minor')
    category = models.CharField(max_length=100, blank=True,
                               help_text="e.g., Material Defect, Process Issue, Documentation")
    
    # Detection
    detected_date = models.DateField()
    detected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='non_conformances_detected')
    location = models.CharField(max_length=200, blank=True)
    
    # Responsibility
    responsible_department = models.CharField(max_length=100, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='non_conformances_assigned')
    
    # Impact Assessment
    quantity_affected = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_impact = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    customer_impact = models.BooleanField(default=False)
    
    # Resolution
    immediate_action = models.TextField(blank=True,
                                       help_text="Containment or immediate corrective actions")
    root_cause = models.TextField(blank=True)
    resolution_notes = models.TextField(blank=True)
    resolved_date = models.DateField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Attachments
    attachments = models.TextField(blank=True, help_text="File paths or URLs, comma-separated")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='non_conformances_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-detected_date', '-created_at']
        verbose_name = 'Non-Conformance Report'
        verbose_name_plural = 'Non-Conformance Reports'
        permissions = [
            ('can_close_ncr', 'Can close NCR'),
            ('can_view_all_ncr', 'Can view all NCR'),
        ]
    
    def __str__(self):
        return f"{self.ncr_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.ncr_number:
            # Generate NCR number
            last_ncr = NonConformance.objects.order_by('-id').first()
            if last_ncr and last_ncr.ncr_number:
                try:
                    last_number = int(last_ncr.ncr_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.ncr_number = f"NCR-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('quality:nonconformance_detail', kwargs={'pk': self.pk})
    
    @property
    def days_open(self):
        """Calculate days since detection"""
        from django.utils import timezone
        if self.status in ['resolved', 'closed']:
            if self.resolved_date:
                return (self.resolved_date - self.detected_date).days
        return (timezone.now().date() - self.detected_date).days


class CorrectiveAction(models.Model):
    """Corrective and Preventive Actions (CAPA)"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('implemented', 'Implemented'),
        ('verified', 'Verified'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]
    
    TYPE_CHOICES = [
        ('corrective', 'Corrective Action'),
        ('preventive', 'Preventive Action'),
        ('both', 'Corrective & Preventive'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    capa_number = models.CharField(max_length=50, unique=True, editable=False)
    title = models.CharField(max_length=200)
    action_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='corrective')
    
    # Source
    non_conformance = models.ForeignKey(NonConformance, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='corrective_actions')
    source_description = models.TextField(help_text="Description of the issue or opportunity")
    
    # Root Cause Analysis
    root_cause = models.TextField()
    why_analysis = models.TextField(blank=True, help_text="5 Whys or other RCA method")
    
    # Proposed Action
    proposed_action = models.TextField(help_text="Detailed corrective/preventive action plan")
    expected_outcome = models.TextField()
    
    # Implementation
    implementation_plan = models.TextField(blank=True)
    required_resources = models.TextField(blank=True)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    # Responsibility and Timeline
    responsible_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                          related_name='capa_responsible')
    assigned_team = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                          related_name='capa_team_member')
    
    target_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Verification
    verification_method = models.TextField(blank=True,
                                          help_text="How effectiveness will be verified")
    verification_date = models.DateField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    effectiveness_rating = models.IntegerField(null=True, blank=True,
                                              validators=[MinValueValidator(1), MaxValueValidator(5)],
                                              help_text="1=Not Effective, 5=Very Effective")
    
    # Approval
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='capa_approved')
    approval_date = models.DateField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)
    
    # Attachments
    attachments = models.TextField(blank=True, help_text="File paths or URLs, comma-separated")
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='capa_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-target_date', '-created_at']
        verbose_name = 'Corrective Action (CAPA)'
        verbose_name_plural = 'Corrective Actions (CAPA)'
        permissions = [
            ('can_approve_capa', 'Can approve CAPA'),
            ('can_verify_capa', 'Can verify CAPA effectiveness'),
        ]
    
    def __str__(self):
        return f"{self.capa_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.capa_number:
            # Generate CAPA number
            last_capa = CorrectiveAction.objects.order_by('-id').first()
            if last_capa and last_capa.capa_number:
                try:
                    last_number = int(last_capa.capa_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
            self.capa_number = f"CAPA-{new_number:06d}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('quality:capa_detail', kwargs={'pk': self.pk})
    
    @property
    def is_overdue(self):
        """Check if action is overdue"""
        from django.utils import timezone
        if self.status not in ['implemented', 'verified', 'closed']:
            return timezone.now().date() > self.target_date
        return False
    
    @property
    def days_until_due(self):
        """Days until target date"""
        from django.utils import timezone
        if self.status not in ['implemented', 'verified', 'closed']:
            delta = self.target_date - timezone.now().date()
            return delta.days
        return None
