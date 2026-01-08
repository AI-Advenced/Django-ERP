"""
Business Intelligence & Reporting Models
- Dashboard: Custom analytics dashboards
- KPI: Key Performance Indicators
- Report: Scheduled and ad-hoc reports
- DataSource: Data source connections
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from decimal import Decimal
import json


class DataSource(models.Model):
    """Data sources for BI reporting"""
    
    SOURCE_TYPES = [
        ('database', 'Database'),
        ('api', 'API'),
        ('file', 'File Upload'),
        ('internal', 'Internal Models'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    description = models.TextField(blank=True)
    
    # Connection details (stored as JSON)
    connection_config = models.TextField(default=dict, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    last_sync = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='datasources_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
    
    def __str__(self):
        return self.name


class Dashboard(models.Model):
    """Custom analytics dashboards"""
    
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('shared', 'Shared'),
        ('public', 'Public'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Layout configuration (stored as JSON)
    layout_config = models.TextField(default=dict, blank=True,
                                    help_text="Dashboard layout configuration")
    
    # Widgets/components (stored as JSON array)
    widgets = models.TextField(default=list, blank=True,
                              help_text="Dashboard widgets configuration")
    
    # Access control
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='shared_dashboards')
    
    # Settings
    refresh_interval = models.IntegerField(default=300,
                                          help_text="Auto-refresh interval in seconds")
    is_default = models.BooleanField(default=False,
                                    help_text="Set as default dashboard")
    is_active = models.BooleanField(default=True)
    
    # Tracking
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_dashboards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-updated_at']
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        permissions = [
            ('can_share_dashboard', 'Can share dashboard'),
            ('can_view_all_dashboards', 'Can view all dashboards'),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bi_reporting:dashboard_view', kwargs={'pk': self.pk})


class KPI(models.Model):
    """Key Performance Indicators"""
    
    CATEGORY_CHOICES = [
        ('financial', 'Financial'),
        ('sales', 'Sales'),
        ('operations', 'Operations'),
        ('quality', 'Quality'),
        ('hr', 'Human Resources'),
        ('customer', 'Customer'),
        ('marketing', 'Marketing'),
        ('other', 'Other'),
    ]
    
    CALCULATION_TYPES = [
        ('sum', 'Sum'),
        ('average', 'Average'),
        ('count', 'Count'),
        ('percentage', 'Percentage'),
        ('ratio', 'Ratio'),
        ('custom', 'Custom Formula'),
    ]
    
    TREND_CHOICES = [
        ('up', 'Increasing'),
        ('down', 'Decreasing'),
        ('stable', 'Stable'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # Data Source
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Calculation
    calculation_type = models.CharField(max_length=50, choices=CALCULATION_TYPES)
    formula = models.TextField(blank=True, help_text="Custom calculation formula")
    
    # Current Value
    current_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    previous_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Targets and Thresholds
    target_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    warning_threshold = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    critical_threshold = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Unit and Format
    unit = models.CharField(max_length=50, blank=True, help_text="e.g., $, %, units")
    decimal_places = models.IntegerField(default=2,
                                        validators=[MinValueValidator(0), MaxValueValidator(4)])
    
    # Trend
    trend = models.CharField(max_length=20, choices=TREND_CHOICES, blank=True)
    trend_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    # Update frequency
    update_frequency = models.CharField(max_length=50, default='daily',
                                       help_text="e.g., daily, weekly, monthly")
    last_updated = models.DateTimeField(null=True, blank=True)
    
    # Display settings
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_dashboard = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='kpis_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'display_order', 'name']
        verbose_name = 'KPI'
        verbose_name_plural = 'KPIs'
        permissions = [
            ('can_manage_kpi', 'Can manage KPIs'),
            ('can_view_all_kpi', 'Can view all KPIs'),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('bi_reporting:kpi_detail', kwargs={'pk': self.pk})
    
    @property
    def achievement_percentage(self):
        """Calculate achievement percentage against target"""
        if self.target_value and self.current_value:
            return (self.current_value / self.target_value) * 100
        return None
    
    @property
    def status(self):
        """Determine KPI status based on thresholds"""
        if not self.current_value:
            return 'unknown'
        
        if self.critical_threshold:
            if self.current_value <= self.critical_threshold:
                return 'critical'
        
        if self.warning_threshold:
            if self.current_value <= self.warning_threshold:
                return 'warning'
        
        if self.target_value:
            if self.current_value >= self.target_value:
                return 'good'
            return 'needs_improvement'
        
        return 'normal'
    
    @property
    def variance(self):
        """Calculate variance from previous period"""
        if self.previous_value and self.current_value:
            return self.current_value - self.previous_value
        return None


class KPIHistory(models.Model):
    """Historical KPI values for trend analysis"""
    
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='history')
    
    # Value
    value = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Period
    period_start = models.DateField()
    period_end = models.DateField()
    period_type = models.CharField(max_length=20, default='day',
                                   help_text="day, week, month, quarter, year")
    
    # Metadata
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-period_end']
        verbose_name = 'KPI History'
        verbose_name_plural = 'KPI History'
        unique_together = ['kpi', 'period_start', 'period_end']
    
    def __str__(self):
        return f"{self.kpi.code} - {self.period_end}: {self.value}"


class Report(models.Model):
    """Reports - scheduled and ad-hoc"""
    
    REPORT_TYPES = [
        ('sales', 'Sales Report'),
        ('financial', 'Financial Report'),
        ('inventory', 'Inventory Report'),
        ('hr', 'HR Report'),
        ('quality', 'Quality Report'),
        ('custom', 'Custom Report'),
    ]
    
    FORMAT_CHOICES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('csv', 'CSV'),
        ('html', 'HTML'),
    ]
    
    SCHEDULE_CHOICES = [
        ('manual', 'Manual'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    description = models.TextField(blank=True)
    
    # Data Source
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Report Configuration
    query_config = models.TextField(default=dict, blank=True,
                                   help_text="Report query configuration")
    filters = models.TextField(default=dict, blank=True,
                              help_text="Report filters")
    columns = models.TextField(default=list, blank=True,
                              help_text="Report columns")
    
    # Output
    output_format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='pdf')
    file_path = models.CharField(max_length=500, blank=True)
    
    # Scheduling
    schedule = models.CharField(max_length=20, choices=SCHEDULE_CHOICES, default='manual')
    schedule_time = models.TimeField(null=True, blank=True)
    schedule_day = models.IntegerField(null=True, blank=True,
                                      validators=[MinValueValidator(1), MaxValueValidator(31)])
    
    # Recipients
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='report_recipients')
    email_on_completion = models.BooleanField(default=False)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    last_run = models.DateTimeField(null=True, blank=True)
    next_run = models.DateTimeField(null=True, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                  related_name='reports_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        permissions = [
            ('can_schedule_report', 'Can schedule reports'),
            ('can_view_all_reports', 'Can view all reports'),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bi_reporting:report_detail', kwargs={'pk': self.pk})


class ReportExecution(models.Model):
    """Report execution history"""
    
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name='executions')
    
    # Execution details
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    
    # Status
    status = models.CharField(max_length=20, default='running')
    error_message = models.TextField(blank=True)
    
    # Output
    output_file = models.CharField(max_length=500, blank=True)
    row_count = models.IntegerField(null=True, blank=True)
    file_size = models.BigIntegerField(null=True, blank=True, help_text="File size in bytes")
    
    # Triggered by
    triggered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = 'Report Execution'
        verbose_name_plural = 'Report Executions'
    
    def __str__(self):
        return f"{self.report.name} - {self.started_at}"


class Widget(models.Model):
    """Dashboard widgets"""
    
    WIDGET_TYPES = [
        ('kpi_card', 'KPI Card'),
        ('chart_line', 'Line Chart'),
        ('chart_bar', 'Bar Chart'),
        ('chart_pie', 'Pie Chart'),
        ('chart_area', 'Area Chart'),
        ('table', 'Data Table'),
        ('metric', 'Metric Display'),
        ('gauge', 'Gauge'),
        ('list', 'List'),
    ]
    
    name = models.CharField(max_length=200)
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    description = models.TextField(blank=True)
    
    # Data Configuration
    data_source = models.ForeignKey(DataSource, on_delete=models.SET_NULL, null=True, blank=True)
    kpi = models.ForeignKey(KPI, on_delete=models.SET_NULL, null=True, blank=True)
    query_config = models.TextField(default=dict, blank=True)
    
    # Display Configuration
    display_config = models.TextField(default=dict, blank=True,
                                     help_text="Widget display settings (colors, size, etc.)")
    
    # Refresh
    auto_refresh = models.BooleanField(default=True)
    refresh_interval = models.IntegerField(default=300, help_text="Seconds")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'
    
    def __str__(self):
        return self.name
