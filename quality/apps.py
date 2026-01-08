from django.apps import AppConfig


class QualityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quality'
    verbose_name = 'Quality Management'
    
    def ready(self):
        """Import signals when app is ready"""
        try:
            import quality.signals  # noqa
        except ImportError:
            pass
