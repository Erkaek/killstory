# killstory/apps.py

from django.apps import AppConfig
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import logging

logger = logging.getLogger(__name__)

class KillstoryConfig(AppConfig):
    name = "killstory"
    verbose_name = "Killstory"

    def ready(self):
        # Importer les tâches pour que Celery les détecte
        import killstory.tasks  # noqa: F401

        # Configuration de la tâche cron si elle n'existe pas déjà
        self.setup_periodic_task()

    def setup_periodic_task(self):
        """Configurer une tâche périodique cron pour exécuter populate_killmails tous les jours à minuit."""
        try:
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
                name="Populate killmails daily",
                task="killstory.tasks.populate_killmails",  # Référence complète de la tâche
            )
            logger.info("Tâche cron de population des killmails configurée avec succès.")
        except Exception as e:
            logger.error("Erreur lors de la configuration de la tâche périodique cron : %s", e)
