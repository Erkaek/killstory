# killstory/apps.py

from django.apps import AppConfig

class KillstoryConfig(AppConfig):
    name = "killstory"
    verbose_name = "Killstory"

    def ready(self):
        # Import des tâches pour que Celery les découvre correctement
        import killstory.tasks  # noqa: F401
