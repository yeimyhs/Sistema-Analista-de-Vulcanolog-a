from django.apps import AppConfig


class VolcanoappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'volcanoApp'

    def ready(self):
        import volcanoApp.signals