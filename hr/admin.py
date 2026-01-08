from django.contrib import admin
from .models import (
    Department, Employee, Attendance, LeaveType, LeaveRequest, Payroll,
    JobPosting, Candidate, Interview, TrainingProgram, TrainingEnrollment,
    PerformanceReview
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'manager', 'created_at']
    search_fields = ['name', 'code']
    list_filter = ['created_at']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'department', 'position', 'status', 'hire_date']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    list_filter = ['status', 'department', 'employment_type', 'hire_date']
    date_hierarchy = 'hire_date'


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'check_in_time', 'check_out_time', 'status', 'hours_worked']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    list_filter = ['status', 'date']
    date_hierarchy = 'date'


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'days_allowed', 'is_paid']
    search_fields = ['name', 'code']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['employee', 'leave_type', 'start_date', 'end_date', 'days_requested', 'status', 'created_at']
    search_fields = ['employee__first_name', 'employee__last_name']
    list_filter = ['status', 'leave_type', 'start_date']
    date_hierarchy = 'start_date'


@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ['employee', 'pay_period_start', 'pay_period_end', 'pay_date', 'gross_pay', 'net_pay', 'status']
    search_fields = ['employee__first_name', 'employee__last_name', 'employee__employee_id']
    list_filter = ['status', 'pay_date']
    date_hierarchy = 'pay_date'


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'job_code', 'department', 'employment_type', 'status', 'posted_date', 'closing_date']
    search_fields = ['title', 'job_code']
    list_filter = ['status', 'employment_type', 'department', 'posted_date']
    date_hierarchy = 'posted_date'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'job_posting', 'status', 'rating', 'application_date']
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['status', 'job_posting', 'application_date']
    date_hierarchy = 'application_date'


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'interview_type', 'scheduled_date', 'scheduled_time', 'interviewer', 'status', 'rating']
    search_fields = ['candidate__first_name', 'candidate__last_name']
    list_filter = ['status', 'interview_type', 'scheduled_date']
    date_hierarchy = 'scheduled_date'


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'trainer', 'training_type', 'start_date', 'end_date', 'status']
    search_fields = ['name', 'code', 'trainer']
    list_filter = ['status', 'training_type', 'start_date']
    date_hierarchy = 'start_date'


@admin.register(TrainingEnrollment)
class TrainingEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'training_program', 'status', 'attendance_percentage', 'assessment_score', 'completion_date']
    search_fields = ['employee__first_name', 'employee__last_name', 'training_program__name']
    list_filter = ['status', 'certificate_issued', 'enrollment_date']
    date_hierarchy = 'enrollment_date'


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ['employee', 'reviewer', 'review_date', 'overall_rating', 'status', 'employee_acknowledged']
    search_fields = ['employee__first_name', 'employee__last_name']
    list_filter = ['status', 'review_date', 'employee_acknowledged']
    date_hierarchy = 'review_date'
