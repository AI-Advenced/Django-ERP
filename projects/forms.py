from django import forms
from .models import Project, Task, Milestone, TimeEntry, ProjectDocument


class ProjectForm(forms.ModelForm):
    """
    Form for creating and updating projects
    """
    class Meta:
        model = Project
        fields = [
            'name', 'code', 'description', 'status', 'priority',
            'start_date', 'end_date', 'actual_start_date', 'actual_end_date',
            'estimated_budget', 'actual_budget', 'progress',
            'manager', 'team_members',
            'client_name', 'client_contact', 'client_email',
            'notes', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'actual_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estimated_budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'actual_budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'manager': forms.Select(attrs={'class': 'form-select'}),
            'team_members': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'client_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('End date must be after start date.')
        
        return cleaned_data


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating tasks
    """
    class Meta:
        model = Task
        fields = [
            'project', 'title', 'description', 'status', 'priority',
            'assigned_to', 'start_date', 'due_date', 'completed_date',
            'estimated_hours', 'actual_hours', 'progress',
            'depends_on', 'notes'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estimated_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'actual_hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'progress': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'depends_on': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '5'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        
        if start_date and due_date and start_date > due_date:
            raise forms.ValidationError('Due date must be after start date.')
        
        return cleaned_data


class MilestoneForm(forms.ModelForm):
    """
    Form for creating and updating milestones
    """
    class Meta:
        model = Milestone
        fields = [
            'project', 'name', 'description', 'status',
            'due_date', 'completed_date', 'deliverables', 'notes'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'deliverables': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TimeEntryForm(forms.ModelForm):
    """
    Form for creating time entries
    """
    class Meta:
        model = TimeEntry
        fields = ['task', 'date', 'hours', 'description']
        widgets = {
            'task': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ProjectDocumentForm(forms.ModelForm):
    """
    Form for uploading project documents
    """
    class Meta:
        model = ProjectDocument
        fields = ['project', 'title', 'description', 'file']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
