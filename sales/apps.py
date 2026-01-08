from django.apps import AppConfig


class SalesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales'
    verbose_name = 'Sales Management'

    def ready(self):
        """
        Import signals when the app is ready
        """
        try:
            import sales.signals
        except ImportError:
            pass
