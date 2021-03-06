# Generated by Django 2.2.6 on 2020-03-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0003_auto_20200116_0652'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribedeventtype',
            name='replay_failed_events',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AddField(
            model_name='subscribedeventtype',
            name='replay_missed_events',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='eventprocessingmodule',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
