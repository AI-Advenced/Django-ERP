from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import models
from .models import Task, TimeEntry


@receiver(pre_save, sender=Task)
def update_task_completion_date(sender, instance, **kwargs):
    """
    Automatically set completion date when task status changes to completed
    """
    if instance.status == 'completed' and not instance.completed_date:
        from django.utils import timezone
        instance.completed_date = timezone.now().date()


@receiver(post_save, sender=TimeEntry)
def update_task_actual_hours(sender, instance, created, **kwargs):
    """
    Update task actual hours when a time entry is added
    """
    if created:
        task = instance.task
        total_hours = task.time_entries.aggregate(
            total=models.Sum('hours')
        )['total'] or 0
        task.actual_hours = total_hours
        task.save(update_fields=['actual_hours'])
