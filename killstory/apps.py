import logging
from django.apps import AppConfig


# Configuration du logger pour `apps.py`
logger = logging.getLogger(__name__)

class KillstoryConfig(AppConfig):
    name = "killstory"
    verbose_name = "Killstory"

    def ready(self):
        # Importer les tâches pour que Celery les détecte
        import killstory.tasks  # noqa: F401

        # Configurer la tâche cron si elle n'existe pas déjà
        self.setup_periodic_task()

    def setup_periodic_task(self):
        """Configurer une tâche périodique cron pour exécuter `populate_killmails` tous les jours à 6h00 du matin."""
        try:
            # Importer `PeriodicTask` et `CrontabSchedule` uniquement lorsque l'application est prête
            from django_celery_beat.models import PeriodicTask, CrontabSchedule

            # Création du planning (crontab) pour 6h00 chaque jour
            schedule, _ = CrontabSchedule.objects.get_or_create(
                minute="0",
                hour="6",
                day_of_week="*",  # chaque jour de la semaine
                day_of_month="*",  # chaque jour du mois
                month_of_year="*",  # chaque mois
            )
            # Configurer la tâche périodique
            PeriodicTask.objects.get_or_create(
                crontab=schedule,
                name="Populate killmails daily",  # Nom unique pour la tâche
                task="killstory.tasks.populate_killmails",  # Chemin complet de la tâche
            )
            logger.info("Tâche cron de population des killmails configurée avec succès.")
        except Exception as e:
            logger.error("Erreur lors de la configuration de la tâche périodique cron : %s", e)
