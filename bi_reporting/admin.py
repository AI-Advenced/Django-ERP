"""
Business Intelligence & Reporting Admin Configuration
"""

from django.contrib import admin
from .models import (
    DataSource, Dashboard, KPI, KPIHistory,
    Report, ReportExecution, Widget
)


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """Admin for Data Sources"""
    list_display = ['name', 'source_type', 'is_active', 'last_sync', 'created_at']
    list_filter = ['source_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'last_sync']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'source_type', 'description')
        }),
        ('Configuration', {
            'fields': ('connection_config',)
        }),
        ('Status', {
            'fields': ('is_active', 'last_sync')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    """Admin for Dashboards"""
    list_display = ['name', 'owner', 'visibility', 'is_default', 'is_active', 'created_at']
    list_filter = ['visibility', 'is_default', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['shared_with']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'owner')
        }),
        ('Configuration', {
            'fields': ('layout_config', 'widgets')
        }),
        ('Access Control', {
            'fields': ('visibility', 'shared_with')
        }),
        ('Settings', {
            'fields': ('refresh_interval', 'is_default', 'is_active')
        }),
        ('Tracking', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class KPIHistoryInline(admin.TabularInline):
    """Inline for KPI History"""
    model = KPIHistory
    extra = 1
    fields = ['value', 'period_start', 'period_end', 'period_type']


@admin.register(KPI)
class KPIAdmin(admin.ModelAdmin):
    """Admin for KPIs"""
    list_display = [
        'code', 'name', 'category', 'current_value', 'target_value',
        'trend', 'status', 'is_active', 'show_on_dashboard'
    ]
    list_filter = ['category', 'trend', 'is_active', 'show_on_dashboard', 'created_at']
    search_fields = ['name', 'code', 'description']
    readonly_fields = ['created_at', 'updated_at', 'last_updated']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description', 'category')
        }),
        ('Data Source', {
            'fields': ('data_source', 'calculation_type', 'formula')
        }),
        ('Values', {
            'fields': ('current_value', 'previous_value', 'target_value')
        }),
        ('Thresholds', {
            'fields': ('warning_threshold', 'critical_threshold')
        }),
        ('Display', {
            'fields': ('unit', 'decimal_places', 'trend', 'trend_percentage')
        }),
        ('Settings', {
            'fields': (
                'update_frequency', 'last_updated', 'display_order',
                'is_active', 'show_on_dashboard'
            )
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [KPIHistoryInline]


@admin.register(KPIHistory)
class KPIHistoryAdmin(admin.ModelAdmin):
    """Admin for KPI History"""
    list_display = ['kpi', 'value', 'period_start', 'period_end', 'period_type', 'recorded_at']
    list_filter = ['period_type', 'recorded_at', 'kpi__category']
    search_fields = ['kpi__name', 'kpi__code', 'notes']
    date_hierarchy = 'period_end'
    readonly_fields = ['recorded_at']


class ReportExecutionInline(admin.TabularInline):
    """Inline for Report Executions"""
    model = ReportExecution
    extra = 0
    fields = ['started_at', 'status', 'duration_seconds', 'row_count']
    readonly_fields = ['started_at', 'status', 'duration_seconds', 'row_count']


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    """Admin for Reports"""
    list_display = [
        'name', 'report_type', 'schedule', 'status',
        'last_run', 'is_active', 'created_by'
    ]
    list_filter = ['report_type', 'schedule', 'status', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['recipients']
    readonly_fields = ['last_run', 'next_run', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'report_type', 'description')
        }),
        ('Data Source', {
            'fields': ('data_source', 'query_config', 'filters', 'columns')
        }),
        ('Output', {
            'fields': ('output_format', 'file_path')
        }),
        ('Scheduling', {
            'fields': (
                'schedule', 'schedule_time', 'schedule_day',
                'last_run', 'next_run'
            )
        }),
        ('Recipients', {
            'fields': ('recipients', 'email_on_completion')
        }),
        ('Status', {
            'fields': ('status', 'is_active')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ReportExecutionInline]


@admin.register(ReportExecution)
class ReportExecutionAdmin(admin.ModelAdmin):
    """Admin for Report Executions"""
    list_display = [
        'report', 'started_at', 'status', 'duration_seconds',
        'row_count', 'triggered_by'
    ]
    list_filter = ['status', 'started_at']
    search_fields = ['report__name', 'error_message']
    date_hierarchy = 'started_at'
    readonly_fields = ['started_at', 'completed_at', 'duration_seconds']


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """Admin for Widgets"""
    list_display = ['name', 'widget_type', 'auto_refresh', 'is_active', 'created_at']
    list_filter = ['widget_type', 'auto_refresh', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'widget_type', 'description')
        }),
        ('Data Configuration', {
            'fields': ('data_source', 'kpi', 'query_config')
        }),
        ('Display Configuration', {
            'fields': ('display_config',)
        }),
        ('Refresh Settings', {
            'fields': ('auto_refresh', 'refresh_interval')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
