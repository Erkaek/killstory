from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Killmail',
            fields=[
                ('killmail_id', models.IntegerField(primary_key=True, serialize=False)),
                ('killmail_time', models.DateTimeField()),
                ('solar_system_id', models.IntegerField()),
                ('moon_id', models.IntegerField(blank=True, null=True)),
                ('war_id', models.IntegerField(blank=True, null=True)),
                ('position_x', models.FloatField(blank=True, null=True)),
                ('position_y', models.FloatField(blank=True, null=True)),
                ('position_z', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'kill_killmail',
            },
        ),
    ]
