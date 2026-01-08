from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    Department, Employee, Attendance, LeaveType, LeaveRequest, Payroll,
    JobPosting, Candidate, Interview, TrainingProgram, TrainingEnrollment,
    PerformanceReview
)
from .forms import (
    DepartmentForm, EmployeeForm, AttendanceForm, LeaveTypeForm, LeaveRequestForm,
    PayrollForm, JobPostingForm, CandidateForm, InterviewForm, TrainingProgramForm,
    TrainingEnrollmentForm, PerformanceReviewForm
)


@login_required
def hr_dashboard(request):
    """HR Dashboard with key metrics"""
    context = {
        'total_employees': Employee.objects.filter(status='active').count(),
        'total_departments': Department.objects.count(),
        'pending_leave_requests': LeaveRequest.objects.filter(status='pending').count(),
        'active_job_postings': JobPosting.objects.filter(status='active').count(),
        'recent_hires': Employee.objects.order_by('-hire_date')[:5],
        'pending_interviews': Interview.objects.filter(status='scheduled').count(),
        'ongoing_trainings': TrainingProgram.objects.filter(status='ongoing').count(),
    }
    return render(request, 'hr/dashboard.html', context)


# ==================== EMPLOYEE VIEWS ====================

@login_required
def employee_list(request):
    """List all employees with filters"""
    employees = Employee.objects.select_related('department', 'manager').all()
    
    # Apply filters
    search_query = request.GET.get('search', '')
    department_filter = request.GET.get('department', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        employees = employees.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    
    if status_filter:
        employees = employees.filter(status=status_filter)
    
    departments = Department.objects.all()
    
    context = {
        'employees': employees,
        'departments': departments,
        'search_query': search_query,
        'department_filter': department_filter,
        'status_filter': status_filter,
    }
    return render(request, 'hr/employee_list.html', context)


@login_required
def employee_detail(request, pk):
    """Employee detail view"""
    employee = get_object_or_404(Employee, pk=pk)
    context = {
        'employee': employee,
        'recent_attendance': employee.attendances.order_by('-date')[:10],
        'recent_leaves': employee.leave_requests.order_by('-created_at')[:5],
        'recent_payrolls': employee.payrolls.order_by('-pay_date')[:5],
    }
    return render(request, 'hr/employee_detail.html', context)


@login_required
def employee_create(request):
    """Create new employee"""
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.full_name} created successfully.')
            return redirect('hr:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/employee_form.html', context)


@login_required
def employee_update(request, pk):
    """Update employee"""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.full_name} updated successfully.')
            return redirect('hr:employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    
    context = {'form': form, 'employee': employee, 'action': 'Update'}
    return render(request, 'hr/employee_form.html', context)


@login_required
def employee_delete(request, pk):
    """Delete employee"""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee_name = employee.full_name
        employee.delete()
        messages.success(request, f'Employee {employee_name} deleted successfully.')
        return redirect('hr:employee_list')
    
    context = {'employee': employee}
    return render(request, 'hr/employee_confirm_delete.html', context)


# ==================== DEPARTMENT VIEWS ====================

@login_required
def department_list(request):
    """List all departments"""
    departments = Department.objects.annotate(employee_count=Count('employees')).all()
    context = {'departments': departments}
    return render(request, 'hr/department_list.html', context)


@login_required
def department_detail(request, pk):
    """Department detail view"""
    department = get_object_or_404(Department, pk=pk)
    employees = department.employees.all()
    context = {'department': department, 'employees': employees}
    return render(request, 'hr/department_detail.html', context)


@login_required
def department_create(request):
    """Create new department"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department {department.name} created successfully.')
            return redirect('hr:department_detail', pk=department.pk)
    else:
        form = DepartmentForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/department_form.html', context)


@login_required
def department_update(request, pk):
    """Update department"""
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Department {department.name} updated successfully.')
            return redirect('hr:department_detail', pk=department.pk)
    else:
        form = DepartmentForm(instance=department)
    
    context = {'form': form, 'department': department, 'action': 'Update'}
    return render(request, 'hr/department_form.html', context)


@login_required
def department_delete(request, pk):
    """Delete department"""
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department_name = department.name
        department.delete()
        messages.success(request, f'Department {department_name} deleted successfully.')
        return redirect('hr:department_list')
    
    context = {'department': department}
    return render(request, 'hr/department_confirm_delete.html', context)


# ==================== ATTENDANCE VIEWS ====================

@login_required
def attendance_list(request):
    """List attendance records"""
    attendances = Attendance.objects.select_related('employee').all()
    
    # Apply filters
    employee_filter = request.GET.get('employee', '')
    status_filter = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if employee_filter:
        attendances = attendances.filter(employee_id=employee_filter)
    
    if status_filter:
        attendances = attendances.filter(status=status_filter)
    
    if date_from:
        attendances = attendances.filter(date__gte=date_from)
    
    if date_to:
        attendances = attendances.filter(date__lte=date_to)
    
    employees = Employee.objects.filter(status='active')
    
    context = {
        'attendances': attendances[:100],  # Limit to 100 records
        'employees': employees,
        'employee_filter': employee_filter,
        'status_filter': status_filter,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'hr/attendance_list.html', context)


@login_required
def attendance_create(request):
    """Create attendance record"""
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, 'Attendance record created successfully.')
            return redirect('hr:attendance_list')
    else:
        form = AttendanceForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/attendance_form.html', context)


@login_required
def attendance_update(request, pk):
    """Update attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            attendance = form.save()
            messages.success(request, 'Attendance record updated successfully.')
            return redirect('hr:attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    
    context = {'form': form, 'attendance': attendance, 'action': 'Update'}
    return render(request, 'hr/attendance_form.html', context)


@login_required
def attendance_delete(request, pk):
    """Delete attendance record"""
    attendance = get_object_or_404(Attendance, pk=pk)
    
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('hr:attendance_list')
    
    context = {'attendance': attendance}
    return render(request, 'hr/attendance_confirm_delete.html', context)


# ==================== LEAVE REQUEST VIEWS ====================

@login_required
def leave_request_list(request):
    """List leave requests"""
    leave_requests = LeaveRequest.objects.select_related('employee', 'leave_type').all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        leave_requests = leave_requests.filter(status=status_filter)
    
    context = {
        'leave_requests': leave_requests,
        'status_filter': status_filter,
    }
    return render(request, 'hr/leave_request_list.html', context)


@login_required
def leave_request_detail(request, pk):
    """Leave request detail"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    context = {'leave_request': leave_request}
    return render(request, 'hr/leave_request_detail.html', context)


@login_required
def leave_request_create(request):
    """Create leave request"""
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save()
            messages.success(request, 'Leave request created successfully.')
            return redirect('hr:leave_request_detail', pk=leave_request.pk)
    else:
        form = LeaveRequestForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/leave_request_form.html', context)


@login_required
def leave_request_update(request, pk):
    """Update leave request"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request = form.save()
            messages.success(request, 'Leave request updated successfully.')
            return redirect('hr:leave_request_detail', pk=leave_request.pk)
    else:
        form = LeaveRequestForm(instance=leave_request)
    
    context = {'form': form, 'leave_request': leave_request, 'action': 'Update'}
    return render(request, 'hr/leave_request_form.html', context)


@login_required
def leave_request_delete(request, pk):
    """Delete leave request"""
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        leave_request.delete()
        messages.success(request, 'Leave request deleted successfully.')
        return redirect('hr:leave_request_list')
    
    context = {'leave_request': leave_request}
    return render(request, 'hr/leave_request_confirm_delete.html', context)


# ==================== PAYROLL VIEWS ====================

@login_required
def payroll_list(request):
    """List payroll records"""
    payrolls = Payroll.objects.select_related('employee').all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        payrolls = payrolls.filter(status=status_filter)
    
    context = {
        'payrolls': payrolls,
        'status_filter': status_filter,
    }
    return render(request, 'hr/payroll_list.html', context)


@login_required
def payroll_detail(request, pk):
    """Payroll detail"""
    payroll = get_object_or_404(Payroll, pk=pk)
    context = {'payroll': payroll}
    return render(request, 'hr/payroll_detail.html', context)


@login_required
def payroll_create(request):
    """Create payroll record"""
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.processed_by = request.user
            payroll.save()
            messages.success(request, 'Payroll record created successfully.')
            return redirect('hr:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/payroll_form.html', context)


@login_required
def payroll_update(request, pk):
    """Update payroll record"""
    payroll = get_object_or_404(Payroll, pk=pk)
    
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            payroll = form.save()
            messages.success(request, 'Payroll record updated successfully.')
            return redirect('hr:payroll_detail', pk=payroll.pk)
    else:
        form = PayrollForm(instance=payroll)
    
    context = {'form': form, 'payroll': payroll, 'action': 'Update'}
    return render(request, 'hr/payroll_form.html', context)


@login_required
def payroll_delete(request, pk):
    """Delete payroll record"""
    payroll = get_object_or_404(Payroll, pk=pk)
    
    if request.method == 'POST':
        payroll.delete()
        messages.success(request, 'Payroll record deleted successfully.')
        return redirect('hr:payroll_list')
    
    context = {'payroll': payroll}
    return render(request, 'hr/payroll_confirm_delete.html', context)


# ==================== RECRUITMENT VIEWS ====================

@login_required
def job_posting_list(request):
    """List job postings"""
    job_postings = JobPosting.objects.select_related('department').annotate(
        candidate_count=Count('candidates')
    ).all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        job_postings = job_postings.filter(status=status_filter)
    
    context = {
        'job_postings': job_postings,
        'status_filter': status_filter,
    }
    return render(request, 'hr/job_posting_list.html', context)


@login_required
def job_posting_detail(request, pk):
    """Job posting detail"""
    job_posting = get_object_or_404(JobPosting, pk=pk)
    candidates = job_posting.candidates.all()
    context = {'job_posting': job_posting, 'candidates': candidates}
    return render(request, 'hr/job_posting_detail.html', context)


@login_required
def job_posting_create(request):
    """Create job posting"""
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job_posting = form.save(commit=False)
            job_posting.created_by = request.user
            job_posting.save()
            messages.success(request, f'Job posting {job_posting.title} created successfully.')
            return redirect('hr:job_posting_detail', pk=job_posting.pk)
    else:
        form = JobPostingForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/job_posting_form.html', context)


@login_required
def job_posting_update(request, pk):
    """Update job posting"""
    job_posting = get_object_or_404(JobPosting, pk=pk)
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job_posting)
        if form.is_valid():
            job_posting = form.save()
            messages.success(request, f'Job posting {job_posting.title} updated successfully.')
            return redirect('hr:job_posting_detail', pk=job_posting.pk)
    else:
        form = JobPostingForm(instance=job_posting)
    
    context = {'form': form, 'job_posting': job_posting, 'action': 'Update'}
    return render(request, 'hr/job_posting_form.html', context)


@login_required
def job_posting_delete(request, pk):
    """Delete job posting"""
    job_posting = get_object_or_404(JobPosting, pk=pk)
    
    if request.method == 'POST':
        title = job_posting.title
        job_posting.delete()
        messages.success(request, f'Job posting {title} deleted successfully.')
        return redirect('hr:job_posting_list')
    
    context = {'job_posting': job_posting}
    return render(request, 'hr/job_posting_confirm_delete.html', context)


# ==================== CANDIDATE VIEWS ====================

@login_required
def candidate_list(request):
    """List candidates"""
    candidates = Candidate.objects.select_related('job_posting').all()
    
    status_filter = request.GET.get('status', '')
    job_filter = request.GET.get('job', '')
    
    if status_filter:
        candidates = candidates.filter(status=status_filter)
    
    if job_filter:
        candidates = candidates.filter(job_posting_id=job_filter)
    
    job_postings = JobPosting.objects.filter(status='active')
    
    context = {
        'candidates': candidates,
        'status_filter': status_filter,
        'job_filter': job_filter,
        'job_postings': job_postings,
    }
    return render(request, 'hr/candidate_list.html', context)


@login_required
def candidate_detail(request, pk):
    """Candidate detail"""
    candidate = get_object_or_404(Candidate, pk=pk)
    interviews = candidate.interviews.all()
    context = {'candidate': candidate, 'interviews': interviews}
    return render(request, 'hr/candidate_detail.html', context)


@login_required
def candidate_create(request):
    """Create candidate"""
    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f'Candidate {candidate.full_name} created successfully.')
            return redirect('hr:candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/candidate_form.html', context)


@login_required
def candidate_update(request, pk):
    """Update candidate"""
    candidate = get_object_or_404(Candidate, pk=pk)
    
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f'Candidate {candidate.full_name} updated successfully.')
            return redirect('hr:candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm(instance=candidate)
    
    context = {'form': form, 'candidate': candidate, 'action': 'Update'}
    return render(request, 'hr/candidate_form.html', context)


@login_required
def candidate_delete(request, pk):
    """Delete candidate"""
    candidate = get_object_or_404(Candidate, pk=pk)
    
    if request.method == 'POST':
        name = candidate.full_name
        candidate.delete()
        messages.success(request, f'Candidate {name} deleted successfully.')
        return redirect('hr:candidate_list')
    
    context = {'candidate': candidate}
    return render(request, 'hr/candidate_confirm_delete.html', context)


# ==================== INTERVIEW VIEWS ====================

@login_required
def interview_list(request):
    """List interviews"""
    interviews = Interview.objects.select_related('candidate', 'interviewer').all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        interviews = interviews.filter(status=status_filter)
    
    context = {
        'interviews': interviews,
        'status_filter': status_filter,
    }
    return render(request, 'hr/interview_list.html', context)


@login_required
def interview_detail(request, pk):
    """Interview detail"""
    interview = get_object_or_404(Interview, pk=pk)
    context = {'interview': interview}
    return render(request, 'hr/interview_detail.html', context)


@login_required
def interview_create(request):
    """Create interview"""
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()
            messages.success(request, 'Interview scheduled successfully.')
            return redirect('hr:interview_detail', pk=interview.pk)
    else:
        form = InterviewForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/interview_form.html', context)


@login_required
def interview_update(request, pk):
    """Update interview"""
    interview = get_object_or_404(Interview, pk=pk)
    
    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            interview = form.save()
            messages.success(request, 'Interview updated successfully.')
            return redirect('hr:interview_detail', pk=interview.pk)
    else:
        form = InterviewForm(instance=interview)
    
    context = {'form': form, 'interview': interview, 'action': 'Update'}
    return render(request, 'hr/interview_form.html', context)


@login_required
def interview_delete(request, pk):
    """Delete interview"""
    interview = get_object_or_404(Interview, pk=pk)
    
    if request.method == 'POST':
        interview.delete()
        messages.success(request, 'Interview deleted successfully.')
        return redirect('hr:interview_list')
    
    context = {'interview': interview}
    return render(request, 'hr/interview_confirm_delete.html', context)


# ==================== TRAINING VIEWS ====================

@login_required
def training_program_list(request):
    """List training programs"""
    training_programs = TrainingProgram.objects.annotate(
        enrollment_count=Count('enrollments')
    ).all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        training_programs = training_programs.filter(status=status_filter)
    
    context = {
        'training_programs': training_programs,
        'status_filter': status_filter,
    }
    return render(request, 'hr/training_program_list.html', context)


@login_required
def training_program_detail(request, pk):
    """Training program detail"""
    training_program = get_object_or_404(TrainingProgram, pk=pk)
    enrollments = training_program.enrollments.select_related('employee').all()
    context = {'training_program': training_program, 'enrollments': enrollments}
    return render(request, 'hr/training_program_detail.html', context)


@login_required
def training_program_create(request):
    """Create training program"""
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST)
        if form.is_valid():
            training_program = form.save()
            messages.success(request, f'Training program {training_program.name} created successfully.')
            return redirect('hr:training_program_detail', pk=training_program.pk)
    else:
        form = TrainingProgramForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/training_program_form.html', context)


@login_required
def training_program_update(request, pk):
    """Update training program"""
    training_program = get_object_or_404(TrainingProgram, pk=pk)
    
    if request.method == 'POST':
        form = TrainingProgramForm(request.POST, instance=training_program)
        if form.is_valid():
            training_program = form.save()
            messages.success(request, f'Training program {training_program.name} updated successfully.')
            return redirect('hr:training_program_detail', pk=training_program.pk)
    else:
        form = TrainingProgramForm(instance=training_program)
    
    context = {'form': form, 'training_program': training_program, 'action': 'Update'}
    return render(request, 'hr/training_program_form.html', context)


@login_required
def training_program_delete(request, pk):
    """Delete training program"""
    training_program = get_object_or_404(TrainingProgram, pk=pk)
    
    if request.method == 'POST':
        name = training_program.name
        training_program.delete()
        messages.success(request, f'Training program {name} deleted successfully.')
        return redirect('hr:training_program_list')
    
    context = {'training_program': training_program}
    return render(request, 'hr/training_program_confirm_delete.html', context)


# ==================== PERFORMANCE REVIEW VIEWS ====================

@login_required
def performance_review_list(request):
    """List performance reviews"""
    reviews = PerformanceReview.objects.select_related('employee', 'reviewer').all()
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        reviews = reviews.filter(status=status_filter)
    
    context = {
        'reviews': reviews,
        'status_filter': status_filter,
    }
    return render(request, 'hr/performance_review_list.html', context)


@login_required
def performance_review_detail(request, pk):
    """Performance review detail"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    context = {'review': review}
    return render(request, 'hr/performance_review_detail.html', context)


@login_required
def performance_review_create(request):
    """Create performance review"""
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Performance review created successfully.')
            return redirect('hr:performance_review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'hr/performance_review_form.html', context)


@login_required
def performance_review_update(request, pk):
    """Update performance review"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    
    if request.method == 'POST':
        form = PerformanceReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            messages.success(request, 'Performance review updated successfully.')
            return redirect('hr:performance_review_detail', pk=review.pk)
    else:
        form = PerformanceReviewForm(instance=review)
    
    context = {'form': form, 'review': review, 'action': 'Update'}
    return render(request, 'hr/performance_review_form.html', context)


@login_required
def performance_review_delete(request, pk):
    """Delete performance review"""
    review = get_object_or_404(PerformanceReview, pk=pk)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Performance review deleted successfully.')
        return redirect('hr:performance_review_list')
    
    context = {'review': review}
    return render(request, 'hr/performance_review_confirm_delete.html', context)
