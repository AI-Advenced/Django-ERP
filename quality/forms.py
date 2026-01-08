"""
Quality Management Forms
"""

from django import forms
from .models import (
    InspectionType, Inspection, InspectionCheckpoint,
    NonConformance, CorrectiveAction
)


class InspectionTypeForm(forms.ModelForm):
    """Form for Inspection Type"""
    
    class Meta:
        model = InspectionType
        fields = ['name', 'code', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class InspectionForm(forms.ModelForm):
    """Form for Quality Inspection"""
    
    class Meta:
        model = Inspection
        fields = [
            'inspection_type', 'title', 'description',
            'reference_type', 'reference_number',
            'scheduled_date', 'scheduled_time',
            'inspector', 'supervisor',
            'status', 'priority',
            'overall_result', 'score', 'notes'
        ]
        widgets = {
            'inspection_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'reference_type': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'inspector': forms.Select(attrs={'class': 'form-select'}),
            'supervisor': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'overall_result': forms.Select(attrs={'class': 'form-select'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class InspectionCheckpointForm(forms.ModelForm):
    """Form for Inspection Checkpoint"""
    
    class Meta:
        model = InspectionCheckpoint
        fields = [
            'sequence', 'checkpoint_name', 'description',
            'acceptance_criteria', 'measurement_method',
            'result', 'measured_value', 'observations'
        ]
        widgets = {
            'sequence': forms.NumberInput(attrs={'class': 'form-control'}),
            'checkpoint_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'acceptance_criteria': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'measurement_method': forms.TextInput(attrs={'class': 'form-control'}),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'measured_value': forms.TextInput(attrs={'class': 'form-control'}),
            'observations': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class NonConformanceForm(forms.ModelForm):
    """Form for Non-Conformance Report"""
    
    class Meta:
        model = NonConformance
        fields = [
            'title', 'description', 'source', 'inspection',
            'reference_type', 'reference_number',
            'severity', 'category',
            'detected_date', 'detected_by', 'location',
            'responsible_department', 'assigned_to',
            'quantity_affected', 'cost_impact', 'customer_impact',
            'immediate_action', 'root_cause', 'resolution_notes',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'source': forms.Select(attrs={'class': 'form-select'}),
            'inspection': forms.Select(attrs={'class': 'form-select'}),
            'reference_type': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'severity': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'detected_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'detected_by': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_department': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'quantity_affected': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cost_impact': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'customer_impact': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'immediate_action': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'root_cause': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'resolution_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class CorrectiveActionForm(forms.ModelForm):
    """Form for Corrective Action (CAPA)"""
    
    class Meta:
        model = CorrectiveAction
        fields = [
            'title', 'action_type', 'non_conformance',
            'source_description', 'root_cause', 'why_analysis',
            'proposed_action', 'expected_outcome',
            'implementation_plan', 'required_resources', 'estimated_cost',
            'responsible_person', 'assigned_team',
            'target_date', 'status', 'priority',
            'verification_method'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'action_type': forms.Select(attrs={'class': 'form-select'}),
            'non_conformance': forms.Select(attrs={'class': 'form-select'}),
            'source_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'root_cause': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'why_analysis': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'proposed_action': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'expected_outcome': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'implementation_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'required_resources': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'responsible_person': forms.Select(attrs={'class': 'form-select'}),
            'assigned_team': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'verification_method': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
