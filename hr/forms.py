from django import forms
from .models import (
    Department, Employee, Attendance, LeaveType, LeaveRequest, Payroll,
    JobPosting, Candidate, Interview, TrainingProgram, TrainingEnrollment,
    PerformanceReview
)


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'manager', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'employee_id', 'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'zip_code', 'country',
            'department', 'position', 'employment_type', 'status', 'hire_date', 
            'termination_date', 'manager', 'salary', 'salary_currency',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship'
        ]
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'termination_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'manager': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_currency': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'check_in_time', 'check_out_time', 'status', 'hours_worked', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'hours_worked': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class LeaveTypeForm(forms.ModelForm):
    class Meta:
        model = LeaveType
        fields = ['name', 'code', 'days_allowed', 'description', 'is_paid']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'days_allowed': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'days_requested', 'reason', 
                  'status', 'approved_by', 'approval_notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'leave_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'days_requested': forms.NumberInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'approved_by': forms.Select(attrs={'class': 'form-control'}),
            'approval_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'pay_period_start', 'pay_period_end', 'pay_date',
            'basic_salary', 'allowances', 'overtime_pay', 'bonuses',
            'tax_deduction', 'insurance_deduction', 'retirement_deduction', 'other_deductions',
            'status', 'notes'
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'pay_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pay_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'allowances': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'overtime_pay': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bonuses': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tax_deduction': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'insurance_deduction': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'retirement_deduction': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'other_deductions': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title', 'job_code', 'department', 'employment_type', 'location', 'positions',
            'description', 'requirements', 'responsibilities',
            'salary_min', 'salary_max', 'salary_currency',
            'status', 'posted_date', 'closing_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'job_code': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'positions': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'salary_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'salary_currency': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'posted_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'closing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            'job_posting', 'first_name', 'last_name', 'email', 'phone',
            'resume', 'cover_letter', 'status',
            'current_salary', 'expected_salary', 'notes', 'rating'
        ]
        widgets = {
            'job_posting': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'current_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expected_salary': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'candidate', 'interview_type', 'scheduled_date', 'scheduled_time', 'duration_minutes',
            'interviewer', 'location', 'meeting_link', 'status',
            'feedback', 'rating', 'recommendation'
        ]
        widgets = {
            'candidate': forms.Select(attrs={'class': 'form-control'}),
            'interview_type': forms.Select(attrs={'class': 'form-control'}),
            'scheduled_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'scheduled_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'interviewer': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'recommendation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TrainingProgramForm(forms.ModelForm):
    class Meta:
        model = TrainingProgram
        fields = [
            'name', 'code', 'description', 'objectives', 'trainer', 'training_type',
            'start_date', 'end_date', 'duration_hours', 'location', 'max_participants',
            'cost_per_participant', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'training_type': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'cost_per_participant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class TrainingEnrollmentForm(forms.ModelForm):
    class Meta:
        model = TrainingEnrollment
        fields = [
            'training_program', 'employee', 'status', 'attendance_percentage',
            'assessment_score', 'completion_date', 'certificate_issued', 'feedback', 'notes'
        ]
        widgets = {
            'training_program': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'attendance_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'assessment_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certificate_issued': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'reviewer', 'review_period_start', 'review_period_end', 'review_date', 'status',
            'technical_skills', 'communication', 'teamwork', 'leadership', 'productivity',
            'strengths', 'areas_for_improvement', 'goals', 'comments',
            'employee_comments', 'employee_acknowledged'
        ]
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'reviewer': forms.Select(attrs={'class': 'form-control'}),
            'review_period_start': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'review_period_end': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'review_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'technical_skills': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'communication': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'teamwork': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'leadership': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'productivity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '5'}),
            'strengths': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'areas_for_improvement': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'goals': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'employee_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'employee_acknowledged': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
