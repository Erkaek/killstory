from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('killstory', '0001_create_killmail'),  # Dépend également de 0001_create_killmail
    ]

    operations = [
        migrations.CreateModel(
            name='Attacker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alliance_id', models.IntegerField(blank=True, null=True)),
                ('character_id', models.IntegerField(blank=True, null=True)),
                ('corporation_id', models.IntegerField(blank=True, null=True)),
                ('faction_id', models.IntegerField(blank=True, null=True)),
                ('damage_done', models.IntegerField()),
                ('final_blow', models.BooleanField()),
                ('security_status', models.FloatField()),
                ('ship_type_id', models.IntegerField()),
                ('weapon_type_id', models.IntegerField()),
                ('killmail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attackers', to='killstory.killmail')),
            ],
            options={
                'db_table': 'kill_attacker',
            },
        ),
    ]
