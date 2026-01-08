"""
Maintenance & Asset Management Forms
"""

from django import forms
from .models import Asset, AssetCategory, PreventiveMaintenance, WorkOrder, MaintenanceLog


class AssetCategoryForm(forms.ModelForm):
    """Form for Asset Category"""
    
    class Meta:
        model = AssetCategory
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AssetForm(forms.ModelForm):
    """Form for Asset/Equipment"""
    
    class Meta:
        model = Asset
        fields = [
            'name', 'category', 'description',
            'manufacturer', 'model_number', 'serial_number', 'year_manufactured',
            'location', 'department', 'assigned_to',
            'purchase_date', 'purchase_cost', 'current_value', 'depreciation_rate',
            'status', 'condition',
            'warranty_expiry', 'service_contract_number', 'service_provider',
            'maintenance_interval_days',
            'specifications', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control'}),
            'model_number': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'year_manufactured': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'purchase_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'purchase_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'depreciation_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'warranty_expiry': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'service_contract_number': forms.TextInput(attrs={'class': 'form-control'}),
            'service_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'maintenance_interval_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'specifications': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PreventiveMaintenanceForm(forms.ModelForm):
    """Form for Preventive Maintenance"""
    
    class Meta:
        model = PreventiveMaintenance
        fields = [
            'title', 'asset', 'description', 'procedure',
            'frequency', 'interval_days', 'start_date', 'next_due_date',
            'assigned_technician', 'estimated_duration_hours',
            'required_parts', 'required_tools', 'estimated_cost',
            'checklist', 'status', 'is_critical',
            'notify_days_before', 'notification_emails'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'procedure': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'frequency': forms.Select(attrs={'class': 'form-select'}),
            'interval_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'next_due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'assigned_technician': forms.Select(attrs={'class': 'form-select'}),
            'estimated_duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'required_parts': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'required_tools': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'checklist': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'is_critical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notify_days_before': forms.NumberInput(attrs={'class': 'form-control'}),
            'notification_emails': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class WorkOrderForm(forms.ModelForm):
    """Form for Work Order"""
    
    class Meta:
        model = WorkOrder
        fields = [
            'title', 'work_type', 'asset', 'preventive_maintenance',
            'description', 'problem_reported',
            'priority', 'status',
            'assigned_to', 'assigned_team', 'supervisor',
            'requested_date', 'scheduled_start', 'scheduled_end',
            'estimated_hours', 'estimated_cost',
            'safety_precautions', 'lockout_tagout_required',
            'permit_required', 'permit_number'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'work_type': forms.Select(attrs={'class': 'form-select'}),
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'preventive_maintenance': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'problem_reported': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'assigned_team': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'requested_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'scheduled_end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'safety_precautions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lockout_tagout_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permit_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'permit_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MaintenanceLogForm(forms.ModelForm):
    """Form for Maintenance Log"""
    
    class Meta:
        model = MaintenanceLog
        fields = [
            'asset', 'work_order', 'log_type', 'date',
            'title', 'description', 'work_performed', 'parts_replaced',
            'technician', 'hours_spent', 'cost',
            'downtime_start', 'downtime_end', 'asset_operational',
            'notes', 'recommendations'
        ]
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-select'}),
            'work_order': forms.Select(attrs={'class': 'form-select'}),
            'log_type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'work_performed': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'parts_replaced': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'technician': forms.Select(attrs={'class': 'form-select'}),
            'hours_spent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'downtime_start': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'downtime_end': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'asset_operational': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
