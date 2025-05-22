# userupdates/apps.py
from django.apps import AppConfig

class UserupdatesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userupdates'

    def ready(self):
        import userupdates.signals  # MUST import your signals here
