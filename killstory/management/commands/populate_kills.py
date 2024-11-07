"""
Django management command to enqueue a task to populate killmails data for owned characters.

This command is used to trigger the asynchronous execution of the `populate_killmails` 
task, which is responsible for fetching and storing killmails data for the characters owned by the user.

When this command is executed, it will enqueue the `populate_killmails` task in 
the background, allowing the task to be processed asynchronously without blocking 
the main application flow.
"""
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
