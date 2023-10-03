from django.apps import AppConfig


class CronometroConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cronometro'
    
    
    def ready(self):
        super().ready()
        from . import signals
