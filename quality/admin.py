"""
Quality Management Admin Configuration
"""

from django.contrib import admin
from .models import (
    InspectionType, Inspection, InspectionCheckpoint,
    NonConformance, CorrectiveAction
)


@admin.register(InspectionType)
class InspectionTypeAdmin(admin.ModelAdmin):
    """Admin for Inspection Types"""
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']


class InspectionCheckpointInline(admin.TabularInline):
    """Inline for Inspection Checkpoints"""
    model = InspectionCheckpoint
    extra = 1
    fields = ['sequence', 'checkpoint_name', 'acceptance_criteria', 'result', 'measured_value']


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    """Admin for Inspections"""
    list_display = [
        'inspection_number', 'title', 'inspection_type', 'status',
        'priority', 'scheduled_date', 'inspector', 'overall_result'
    ]
    list_filter = ['status', 'priority', 'inspection_type', 'scheduled_date', 'overall_result']
    search_fields = ['inspection_number', 'title', 'reference_number']
    readonly_fields = ['inspection_number', 'created_at', 'updated_at']
    date_hierarchy = 'scheduled_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('inspection_number', 'inspection_type', 'title', 'description')
        }),
        ('Reference', {
            'fields': ('reference_type', 'reference_number')
        }),
        ('Scheduling', {
            'fields': ('scheduled_date', 'scheduled_time', 'completed_date')
        }),
        ('Assignment', {
            'fields': ('inspector', 'supervisor')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Results', {
            'fields': ('overall_result', 'score', 'notes')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [InspectionCheckpointInline]


@admin.register(InspectionCheckpoint)
class InspectionCheckpointAdmin(admin.ModelAdmin):
    """Admin for Inspection Checkpoints"""
    list_display = [
        'inspection', 'sequence', 'checkpoint_name', 'result',
        'measured_value', 'checked_by', 'checked_at'
    ]
    list_filter = ['result', 'checked_at', 'inspection__inspection_type']
    search_fields = ['checkpoint_name', 'inspection__inspection_number']
    ordering = ['inspection', 'sequence']


@admin.register(NonConformance)
class NonConformanceAdmin(admin.ModelAdmin):
    """Admin for Non-Conformance Reports"""
    list_display = [
        'ncr_number', 'title', 'source', 'severity', 'status',
        'detected_date', 'detected_by', 'assigned_to'
    ]
    list_filter = ['status', 'severity', 'source', 'detected_date', 'customer_impact']
    search_fields = ['ncr_number', 'title', 'reference_number', 'category']
    readonly_fields = ['ncr_number', 'created_at', 'updated_at']
    date_hierarchy = 'detected_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ncr_number', 'title', 'description')
        }),
        ('Source', {
            'fields': ('source', 'inspection', 'reference_type', 'reference_number')
        }),
        ('Classification', {
            'fields': ('severity', 'category')
        }),
        ('Detection', {
            'fields': ('detected_date', 'detected_by', 'location')
        }),
        ('Responsibility', {
            'fields': ('responsible_department', 'assigned_to')
        }),
        ('Impact Assessment', {
            'fields': ('quantity_affected', 'cost_impact', 'customer_impact')
        }),
        ('Resolution', {
            'fields': ('immediate_action', 'root_cause', 'resolution_notes', 'resolved_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(CorrectiveAction)
class CorrectiveActionAdmin(admin.ModelAdmin):
    """Admin for Corrective Actions (CAPA)"""
    list_display = [
        'capa_number', 'title', 'action_type', 'priority', 'status',
        'responsible_person', 'target_date', 'effectiveness_rating'
    ]
    list_filter = [
        'status', 'action_type', 'priority', 'target_date',
        'effectiveness_rating', 'created_at'
    ]
    search_fields = ['capa_number', 'title', 'root_cause', 'proposed_action']
    readonly_fields = ['capa_number', 'created_at', 'updated_at']
    date_hierarchy = 'target_date'
    filter_horizontal = ['assigned_team']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('capa_number', 'title', 'action_type')
        }),
        ('Source', {
            'fields': ('non_conformance', 'source_description')
        }),
        ('Root Cause Analysis', {
            'fields': ('root_cause', 'why_analysis')
        }),
        ('Proposed Action', {
            'fields': ('proposed_action', 'expected_outcome')
        }),
        ('Implementation', {
            'fields': ('implementation_plan', 'required_resources', 'estimated_cost')
        }),
        ('Responsibility & Timeline', {
            'fields': ('responsible_person', 'assigned_team', 'target_date', 'actual_completion_date')
        }),
        ('Status', {
            'fields': ('status', 'priority')
        }),
        ('Verification', {
            'fields': (
                'verification_method', 'verification_date',
                'verification_notes', 'effectiveness_rating'
            )
        }),
        ('Approval', {
            'fields': ('approved_by', 'approval_date', 'approval_notes')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
