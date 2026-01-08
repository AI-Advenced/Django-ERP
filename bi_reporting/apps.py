from django.apps import AppConfig


class BiReportingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bi_reporting'
    verbose_name = 'Business Intelligence & Reporting'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import bi_reporting.signals  # noqa
        except ImportError:
            pass
