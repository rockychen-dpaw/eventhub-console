# Generated by Django 2.2.9 on 2020-01-16 06:52

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0002_auto_20200116_0650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribedeventtype',
            name='event_type',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='publisher', chained_model_field='publisher', on_delete=django.db.models.deletion.PROTECT, to='console.EventType'),
        ),
    ]
