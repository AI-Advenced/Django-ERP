"""
Business Intelligence & Reporting Signals
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import KPI, KPIHistory, Report, ReportExecution


@receiver(pre_save, sender=KPI)
def update_kpi_trend(sender, instance, **kwargs):
    """Update KPI trend and trend percentage"""
    if instance.pk:
        try:
            old_instance = KPI.objects.get(pk=instance.pk)
            if old_instance.current_value != instance.current_value:
                # Update last_updated
                instance.last_updated = timezone.now()
                
                # Calculate trend
                if instance.previous_value and instance.current_value:
                    if instance.current_value > instance.previous_value:
                        instance.trend = 'up'
                    elif instance.current_value < instance.previous_value:
                        instance.trend = 'down'
                    else:
                        instance.trend = 'stable'
                    
                    # Calculate trend percentage
                    if instance.previous_value != 0:
                        instance.trend_percentage = (
                            (instance.current_value - instance.previous_value) / 
                            instance.previous_value * 100
                        )
        except KPI.DoesNotExist:
            pass


@receiver(post_save, sender=KPI)
def create_kpi_history(sender, instance, created, **kwargs):
    """Auto-create KPI history entry when value changes"""
    if not created and instance.current_value:
        # Check if this is a significant update
        today = timezone.now().date()
        recent_history = KPIHistory.objects.filter(
            kpi=instance,
            period_end=today
        ).first()
        
        if not recent_history:
            # Create history entry
            KPIHistory.objects.create(
                kpi=instance,
                value=instance.current_value,
                period_start=today,
                period_end=today,
                period_type='day',
                recorded_by=instance.created_by
            )


@receiver(post_save, sender=ReportExecution)
def update_report_last_run(sender, instance, created, **kwargs):
    """Update report's last_run timestamp"""
    if instance.status == 'completed':
        Report.objects.filter(pk=instance.report.pk).update(
            last_run=instance.completed_at or instance.started_at
        )
