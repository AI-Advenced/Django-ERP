"""
Business Intelligence & Reporting Forms
"""

from django import forms
from .models import (
    DataSource, Dashboard, KPI, KPIHistory,
    Report, ReportExecution, Widget
)


class DataSourceForm(forms.ModelForm):
    """Form for Data Source"""
    
    class Meta:
        model = DataSource
        fields = ['name', 'source_type', 'description', 'connection_config', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'source_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'connection_config': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DashboardForm(forms.ModelForm):
    """Form for Dashboard"""
    
    class Meta:
        model = Dashboard
        fields = [
            'name', 'description', 'layout_config', 'widgets',
            'visibility', 'shared_with', 'refresh_interval',
            'is_default', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'layout_config': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'widgets': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'visibility': forms.Select(attrs={'class': 'form-select'}),
            'shared_with': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'refresh_interval': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class KPIForm(forms.ModelForm):
    """Form for KPI"""
    
    class Meta:
        model = KPI
        fields = [
            'name', 'code', 'description', 'category',
            'data_source', 'calculation_type', 'formula',
            'current_value', 'previous_value',
            'target_value', 'warning_threshold', 'critical_threshold',
            'unit', 'decimal_places', 'trend', 'trend_percentage',
            'update_frequency', 'display_order',
            'is_active', 'show_on_dashboard'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'data_source': forms.Select(attrs={'class': 'form-select'}),
            'calculation_type': forms.Select(attrs={'class': 'form-select'}),
            'formula': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'previous_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'target_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'warning_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'critical_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'decimal_places': forms.NumberInput(attrs={'class': 'form-control'}),
            'trend': forms.Select(attrs={'class': 'form-select'}),
            'trend_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'update_frequency': forms.TextInput(attrs={'class': 'form-control'}),
            'display_order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_on_dashboard': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class KPIHistoryForm(forms.ModelForm):
    """Form for KPI History"""
    
    class Meta:
        model = KPIHistory
        fields = ['kpi', 'value', 'period_start', 'period_end', 'period_type', 'notes']
        widgets = {
            'kpi': forms.Select(attrs={'class': 'form-select'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'period_type': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ReportForm(forms.ModelForm):
    """Form for Report"""
    
    class Meta:
        model = Report
        fields = [
            'name', 'report_type', 'description',
            'data_source', 'query_config', 'filters', 'columns',
            'output_format', 'schedule', 'schedule_time', 'schedule_day',
            'recipients', 'email_on_completion', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'report_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_source': forms.Select(attrs={'class': 'form-select'}),
            'query_config': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'filters': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'columns': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'output_format': forms.Select(attrs={'class': 'form-select'}),
            'schedule': forms.Select(attrs={'class': 'form-select'}),
            'schedule_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'schedule_day': forms.NumberInput(attrs={'class': 'form-control'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'email_on_completion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class WidgetForm(forms.ModelForm):
    """Form for Widget"""
    
    class Meta:
        model = Widget
        fields = [
            'name', 'widget_type', 'description',
            'data_source', 'kpi', 'query_config',
            'display_config', 'auto_refresh', 'refresh_interval',
            'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'widget_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'data_source': forms.Select(attrs={'class': 'form-select'}),
            'kpi': forms.Select(attrs={'class': 'form-select'}),
            'query_config': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'display_config': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'auto_refresh': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'refresh_interval': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
