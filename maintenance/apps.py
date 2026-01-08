from django.apps import AppConfig


class MaintenanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'maintenance'
    verbose_name = 'Maintenance & Asset Management'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import maintenance.signals  # noqa
        except ImportError:
            pass
