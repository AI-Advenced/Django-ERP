from django.apps import AppConfig


class PurchasingConfig(AppConfig):
    """
    Configuration for the Purchasing & Procurement module.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'purchasing'
    verbose_name = 'Purchasing & Procurement'
    
    def ready(self):
        """
        Import signals when the app is ready.
        """
        try:
            import purchasing.signals
        except ImportError:
            pass
