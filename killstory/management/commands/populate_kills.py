# killstory/management/commands/populate_kills.py

from django.core.management.base import BaseCommand
from killstory.tasks import populate_killmails

class Command(BaseCommand):
    """Django management command to enqueue a task to populate killmails data for owned characters."""
    
    help = 'Enqueue a task to populate killmails data for owned characters'

    def handle(self, *args, **options):
        """Main handler for the command execution."""
        populate_killmails.delay()  # Execute the task asynchronously
        self.stdout.write(self.style.SUCCESS("Killmails population task has been queued in the background."))
