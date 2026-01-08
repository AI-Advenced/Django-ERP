"""
Quality Management Signals
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Inspection, NonConformance, CorrectiveAction


@receiver(post_save, sender=Inspection)
def update_inspection_completion(sender, instance, created, **kwargs):
    """Update completed_date when inspection status changes to completed/passed/failed"""
    if not created and instance.status in ['completed', 'passed', 'failed']:
        if not instance.completed_date:
            instance.completed_date = timezone.now()
            # Avoid recursion by using update instead of save
            Inspection.objects.filter(pk=instance.pk).update(
                completed_date=instance.completed_date
            )


@receiver(post_save, sender=NonConformance)
def update_ncr_resolution(sender, instance, created, **kwargs):
    """Update resolved_date when NCR status changes to resolved/closed"""
    if not created and instance.status in ['resolved', 'closed']:
        if not instance.resolved_date:
            instance.resolved_date = timezone.now().date()
            # Avoid recursion
            NonConformance.objects.filter(pk=instance.pk).update(
                resolved_date=instance.resolved_date
            )


@receiver(post_save, sender=CorrectiveAction)
def update_capa_completion(sender, instance, created, **kwargs):
    """Update actual_completion_date when CAPA status changes to implemented"""
    if not created and instance.status == 'implemented':
        if not instance.actual_completion_date:
            instance.actual_completion_date = timezone.now().date()
            # Avoid recursion
            CorrectiveAction.objects.filter(pk=instance.pk).update(
                actual_completion_date=instance.actual_completion_date
            )


@receiver(pre_save, sender=CorrectiveAction)
def update_approval_info(sender, instance, **kwargs):
    """Update approval date when CAPA is approved"""
    if instance.pk:
        try:
            old_instance = CorrectiveAction.objects.get(pk=instance.pk)
            if old_instance.status != 'approved' and instance.status == 'approved':
                if not instance.approval_date:
                    instance.approval_date = timezone.now().date()
        except CorrectiveAction.DoesNotExist:
            pass
