# killstory/migrations/0006_merge.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('killstory', '0004_create_victimcontaineditem'),
        ('killstory', '0005_create_attacker'),
    ]

    operations = [
        # Il n'y a généralement aucune opération ici car cette migration
        # sert uniquement à fusionner les chemins de migration.
    ]
