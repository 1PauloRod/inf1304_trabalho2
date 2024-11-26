from django.apps import AppConfig


class MtcarsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mtcarsApp'
    
    def ready(self):
        import mtcarsApp.signals
