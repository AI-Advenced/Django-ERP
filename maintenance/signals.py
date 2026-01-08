"""
Maintenance & Asset Management Signals
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import WorkOrder, PreventiveMaintenance, MaintenanceLog, Asset


@receiver(post_save, sender=WorkOrder)
def update_asset_status(sender, instance, created, **kwargs):
    """Update asset status when work order status changes"""
    if not created:
        if instance.status == 'in_progress':
            # Update asset status to maintenance
            if instance.asset.status == 'operational':
                Asset.objects.filter(pk=instance.asset.pk).update(
                    status='maintenance'
                )
        elif instance.status == 'completed':
            # Update asset status back to operational
            Asset.objects.filter(pk=instance.asset.pk).update(
                status='operational',
                last_maintenance_date=timezone.now().date()
            )


@receiver(post_save, sender=WorkOrder)
def update_work_order_dates(sender, instance, created, **kwargs):
    """Auto-update work order dates based on status"""
    if not created:
        updated_fields = {}
        
        if instance.status == 'in_progress' and not instance.actual_start:
            updated_fields['actual_start'] = timezone.now()
        
        if instance.status == 'completed' and not instance.actual_end:
            updated_fields['actual_end'] = timezone.now()
        
        if updated_fields:
            WorkOrder.objects.filter(pk=instance.pk).update(**updated_fields)


@receiver(post_save, sender=PreventiveMaintenance)
def update_pm_schedule(sender, instance, created, **kwargs):
    """Update PM schedule after completion"""
    if not created and instance.last_performed_date:
        # Calculate next due date
        next_date = instance.calculate_next_due_date()
        if next_date != instance.next_due_date:
            PreventiveMaintenance.objects.filter(pk=instance.pk).update(
                next_due_date=next_date
            )


@receiver(post_save, sender=MaintenanceLog)
def update_asset_metrics(sender, instance, created, **kwargs):
    """Update asset metrics when maintenance log is created"""
    if created and instance.downtime_start and instance.downtime_end:
        # Calculate downtime
        downtime = instance.downtime_duration
        
        # Update asset downtime hours
        asset = instance.asset
        asset.downtime_hours = float(asset.downtime_hours) + downtime
        asset.save(update_fields=['downtime_hours'])


@receiver(post_save, sender=WorkOrder)
def create_maintenance_log(sender, instance, created, **kwargs):
    """Create maintenance log when work order is completed"""
    if not created and instance.status == 'completed':
        # Check if log already exists for this work order
        if not MaintenanceLog.objects.filter(work_order=instance).exists():
            MaintenanceLog.objects.create(
                asset=instance.asset,
                work_order=instance,
                log_type='maintenance',
                date=timezone.now().date(),
                title=f"WO Completed: {instance.title}",
                description=instance.description,
                work_performed=instance.resolution or "Work order completed",
                technician=instance.assigned_to,
                hours_spent=instance.actual_hours,
                cost=instance.actual_cost,
                asset_operational=True,
                created_by=instance.assigned_to
            )
