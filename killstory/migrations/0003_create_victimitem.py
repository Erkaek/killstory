from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('killstory', '0002_create_victim'),
    ]

    operations = [
        migrations.CreateModel(
            name='VictimItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type_id', models.IntegerField()),
                ('flag', models.IntegerField()),
                ('quantity_destroyed', models.BigIntegerField(blank=True, null=True)),
                ('quantity_dropped', models.BigIntegerField(blank=True, null=True)),
                ('singleton', models.IntegerField()),
                ('victim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='killstory.victim')),
            ],
            options={
                'db_table': 'kill_victim_item',
            },
        ),
    ]
