from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('killstory', '0003_create_victimitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='VictimContainedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type_id', models.IntegerField()),
                ('flag', models.IntegerField()),
                ('quantity_destroyed', models.BigIntegerField(blank=True, null=True)),
                ('quantity_dropped', models.BigIntegerField(blank=True, null=True)),
                ('singleton', models.IntegerField()),
                ('parent_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contained_items', to='killstory.victimitem')),
            ],
            options={
                'db_table': 'kill_victim_contained_item',
            },
        ),
    ]
