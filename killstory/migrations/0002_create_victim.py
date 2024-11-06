from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('killstory', '0001_create_killmail'),  # Dépend de 0001_create_killmail
    ]

    operations = [
        migrations.CreateModel(
            name='Victim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alliance_id', models.IntegerField(blank=True, null=True)),
                ('character_id', models.IntegerField(blank=True, null=True)),
                ('corporation_id', models.IntegerField(blank=True, null=True)),
                ('faction_id', models.IntegerField(blank=True, null=True)),
                ('damage_taken', models.IntegerField()),
                ('ship_type_id', models.IntegerField()),
                ('killmail', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='victim', to='killstory.killmail')),
            ],
            options={
                'db_table': 'kill_victim',
            },
        ),
    ]
