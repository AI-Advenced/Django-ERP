"""
Django app configuration for Logistics & Supply Chain Management Module
"""
from django.apps import AppConfig


class LogisticsConfig(AppConfig):
    """Configuration for Logistics app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logistics'
    verbose_name = 'Logistics & Supply Chain Management'

    def ready(self):
        """Import signals when app is ready"""
        try:
            import logistics.signals
        except ImportError:
            pass
