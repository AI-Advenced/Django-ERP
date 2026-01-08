"""
Maintenance & Asset Management Admin Configuration
"""

from django.contrib import admin
from .models import AssetCategory, Asset, PreventiveMaintenance, WorkOrder, MaintenanceLog


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    """Admin for Asset Categories"""
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """Admin for Assets"""
    list_display = [
        'asset_number', 'name', 'category', 'status', 'condition',
        'location', 'assigned_to', 'next_maintenance_date'
    ]
    list_filter = ['status', 'condition', 'category', 'location', 'created_at']
    search_fields = ['asset_number', 'name', 'serial_number', 'manufacturer', 'model_number']
    readonly_fields = ['asset_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('asset_number', 'name', 'category', 'description')
        }),
        ('Specifications', {
            'fields': (
                'manufacturer', 'model_number', 'serial_number',
                'year_manufactured', 'specifications'
            )
        }),
        ('Location & Assignment', {
            'fields': ('location', 'department', 'assigned_to')
        }),
        ('Financial Information', {
            'fields': (
                'purchase_date', 'purchase_cost', 'current_value',
                'depreciation_rate'
            )
        }),
        ('Status', {
            'fields': ('status', 'condition')
        }),
        ('Warranty & Service', {
            'fields': (
                'warranty_expiry', 'service_contract_number',
                'service_provider'
            )
        }),
        ('Maintenance', {
            'fields': (
                'last_maintenance_date', 'next_maintenance_date',
                'maintenance_interval_days'
            )
        }),
        ('Operational Metrics', {
            'fields': ('operating_hours', 'downtime_hours')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PreventiveMaintenance)
class PreventiveMaintenanceAdmin(admin.ModelAdmin):
    """Admin for Preventive Maintenance"""
    list_display = [
        'pm_number', 'title', 'asset', 'frequency', 'next_due_date',
        'status', 'is_critical', 'assigned_technician'
    ]
    list_filter = ['status', 'frequency', 'is_critical', 'created_at']
    search_fields = ['pm_number', 'title', 'asset__asset_number', 'description']
    readonly_fields = ['pm_number', 'created_at', 'updated_at']
    date_hierarchy = 'next_due_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('pm_number', 'title', 'asset', 'description', 'procedure')
        }),
        ('Scheduling', {
            'fields': (
                'frequency', 'interval_days', 'start_date',
                'next_due_date', 'last_performed_date'
            )
        }),
        ('Assignment', {
            'fields': ('assigned_technician', 'estimated_duration_hours')
        }),
        ('Resources', {
            'fields': (
                'required_parts', 'required_tools', 'estimated_cost'
            )
        }),
        ('Checklist', {
            'fields': ('checklist',)
        }),
        ('Status', {
            'fields': ('status', 'is_critical')
        }),
        ('Notifications', {
            'fields': ('notify_days_before', 'notification_emails')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    """Admin for Work Orders"""
    list_display = [
        'wo_number', 'title', 'work_type', 'asset', 'priority',
        'status', 'assigned_to', 'requested_date'
    ]
    list_filter = [
        'status', 'priority', 'work_type', 'requested_date', 'created_at'
    ]
    search_fields = ['wo_number', 'title', 'asset__asset_number', 'description']
    readonly_fields = ['wo_number', 'created_at', 'updated_at']
    date_hierarchy = 'requested_date'
    filter_horizontal = ['assigned_team']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('wo_number', 'title', 'work_type', 'asset', 'preventive_maintenance')
        }),
        ('Description', {
            'fields': ('description', 'problem_reported', 'root_cause', 'resolution')
        }),
        ('Priority & Status', {
            'fields': ('priority', 'status')
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'assigned_team', 'supervisor')
        }),
        ('Scheduling', {
            'fields': (
                'requested_date', 'scheduled_start', 'scheduled_end',
                'actual_start', 'actual_end', 'estimated_hours', 'actual_hours'
            )
        }),
        ('Costs', {
            'fields': (
                'estimated_cost', 'actual_cost', 'labor_cost',
                'parts_cost', 'other_cost'
            )
        }),
        ('Parts & Materials', {
            'fields': ('parts_used', 'tools_used')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approval_date', 'approval_notes')
        }),
        ('Completion', {
            'fields': (
                'completion_notes', 'verification_required',
                'verified_by', 'verification_date'
            )
        }),
        ('Safety', {
            'fields': (
                'safety_precautions', 'lockout_tagout_required',
                'permit_required', 'permit_number'
            )
        }),
        ('Tracking', {
            'fields': ('requested_by', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    """Admin for Maintenance Logs"""
    list_display = [
        'asset', 'log_type', 'date', 'title', 'technician',
        'hours_spent', 'cost', 'asset_operational'
    ]
    list_filter = ['log_type', 'date', 'asset_operational', 'created_at']
    search_fields = ['title', 'description', 'asset__asset_number']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('References', {
            'fields': ('asset', 'work_order')
        }),
        ('Log Details', {
            'fields': ('log_type', 'date', 'title', 'description')
        }),
        ('Work Performed', {
            'fields': ('work_performed', 'parts_replaced', 'technician')
        }),
        ('Metrics', {
            'fields': ('hours_spent', 'cost')
        }),
        ('Downtime', {
            'fields': ('downtime_start', 'downtime_end', 'asset_operational')
        }),
        ('Notes', {
            'fields': ('notes', 'recommendations')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
