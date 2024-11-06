# killstory/apps.py

from django.apps import AppConfig

class KillstoryConfig(AppConfig):
    name = 'killstory'
    verbose_name = 'Killstory'

    def ready(self):
        import killstory.tasks  # Importer les tâches lors de la préparation de l'application
