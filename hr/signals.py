from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import LeaveRequest, Payroll, PerformanceReview, Attendance


@receiver(pre_save, sender=LeaveRequest)
def leave_request_pre_save(sender, instance, **kwargs):
    """
    Set approval_date when leave request is approved or rejected
    """
    if instance.pk:
        try:
            old_instance = LeaveRequest.objects.get(pk=instance.pk)
            # If status changed to approved or rejected, set approval_date
            if old_instance.status == 'pending' and instance.status in ['approved', 'rejected']:
                if not instance.approval_date:
                    instance.approval_date = timezone.now()
        except LeaveRequest.DoesNotExist:
            pass


@receiver(post_save, sender=LeaveRequest)
def leave_request_post_save(sender, instance, created, **kwargs):
    """
    Handle post-save operations for leave requests
    """
    if created:
        # You can add notification logic here
        # For example, notify the employee's manager
        pass


@receiver(post_save, sender=Payroll)
def payroll_post_save(sender, instance, created, **kwargs):
    """
    Handle post-save operations for payroll
    """
    if created:
        # You can add notification logic here
        # For example, notify the employee about payroll processing
        pass


@receiver(post_save, sender=PerformanceReview)
def performance_review_post_save(sender, instance, created, **kwargs):
    """
    Handle post-save operations for performance reviews
    """
    if created:
        # You can add notification logic here
        # For example, notify the employee about new review
        pass


@receiver(pre_save, sender=PerformanceReview)
def performance_review_pre_save(sender, instance, **kwargs):
    """
    Set acknowledgement_date when employee acknowledges the review
    """
    if instance.pk:
        try:
            old_instance = PerformanceReview.objects.get(pk=instance.pk)
            # If employee_acknowledged changed from False to True, set acknowledgement_date
            if not old_instance.employee_acknowledged and instance.employee_acknowledged:
                if not instance.acknowledgement_date:
                    instance.acknowledgement_date = timezone.now()
        except PerformanceReview.DoesNotExist:
            pass


@receiver(post_save, sender=Attendance)
def attendance_post_save(sender, instance, created, **kwargs):
    """
    Calculate hours worked if check_in and check_out times are present
    """
    if instance.check_in_time and instance.check_out_time and not instance.hours_worked:
        # Calculate hours worked
        from datetime import datetime, timedelta
        check_in = datetime.combine(instance.date, instance.check_in_time)
        check_out = datetime.combine(instance.date, instance.check_out_time)
        
        # Handle case where check_out is past midnight
        if check_out < check_in:
            check_out += timedelta(days=1)
        
        duration = check_out - check_in
        hours = duration.total_seconds() / 3600
        
        # Update without triggering another signal
        Attendance.objects.filter(pk=instance.pk).update(hours_worked=round(hours, 2))
