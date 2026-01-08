from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # Dashboard
    path('', views.hr_dashboard, name='dashboard'),
    
    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    
    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:pk>/', views.department_detail, name='department_detail'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:pk>/update/', views.department_update, name='department_update'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department_delete'),
    
    # Attendance URLs
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/create/', views.attendance_create, name='attendance_create'),
    path('attendance/<int:pk>/update/', views.attendance_update, name='attendance_update'),
    path('attendance/<int:pk>/delete/', views.attendance_delete, name='attendance_delete'),
    
    # Leave Request URLs
    path('leave-requests/', views.leave_request_list, name='leave_request_list'),
    path('leave-requests/<int:pk>/', views.leave_request_detail, name='leave_request_detail'),
    path('leave-requests/create/', views.leave_request_create, name='leave_request_create'),
    path('leave-requests/<int:pk>/update/', views.leave_request_update, name='leave_request_update'),
    path('leave-requests/<int:pk>/delete/', views.leave_request_delete, name='leave_request_delete'),
    
    # Payroll URLs
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('payroll/create/', views.payroll_create, name='payroll_create'),
    path('payroll/<int:pk>/update/', views.payroll_update, name='payroll_update'),
    path('payroll/<int:pk>/delete/', views.payroll_delete, name='payroll_delete'),
    
    # Job Posting URLs
    path('job-postings/', views.job_posting_list, name='job_posting_list'),
    path('job-postings/<int:pk>/', views.job_posting_detail, name='job_posting_detail'),
    path('job-postings/create/', views.job_posting_create, name='job_posting_create'),
    path('job-postings/<int:pk>/update/', views.job_posting_update, name='job_posting_update'),
    path('job-postings/<int:pk>/delete/', views.job_posting_delete, name='job_posting_delete'),
    
    # Candidate URLs
    path('candidates/', views.candidate_list, name='candidate_list'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('candidates/create/', views.candidate_create, name='candidate_create'),
    path('candidates/<int:pk>/update/', views.candidate_update, name='candidate_update'),
    path('candidates/<int:pk>/delete/', views.candidate_delete, name='candidate_delete'),
    
    # Interview URLs
    path('interviews/', views.interview_list, name='interview_list'),
    path('interviews/<int:pk>/', views.interview_detail, name='interview_detail'),
    path('interviews/create/', views.interview_create, name='interview_create'),
    path('interviews/<int:pk>/update/', views.interview_update, name='interview_update'),
    path('interviews/<int:pk>/delete/', views.interview_delete, name='interview_delete'),
    
    # Training Program URLs
    path('training-programs/', views.training_program_list, name='training_program_list'),
    path('training-programs/<int:pk>/', views.training_program_detail, name='training_program_detail'),
    path('training-programs/create/', views.training_program_create, name='training_program_create'),
    path('training-programs/<int:pk>/update/', views.training_program_update, name='training_program_update'),
    path('training-programs/<int:pk>/delete/', views.training_program_delete, name='training_program_delete'),
    
    # Performance Review URLs
    path('performance-reviews/', views.performance_review_list, name='performance_review_list'),
    path('performance-reviews/<int:pk>/', views.performance_review_detail, name='performance_review_detail'),
    path('performance-reviews/create/', views.performance_review_create, name='performance_review_create'),
    path('performance-reviews/<int:pk>/update/', views.performance_review_update, name='performance_review_update'),
    path('performance-reviews/<int:pk>/delete/', views.performance_review_delete, name='performance_review_delete'),
]
