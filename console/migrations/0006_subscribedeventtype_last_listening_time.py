# Generated by Django 2.2.6 on 2020-03-05 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0005_auto_20200305_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribedeventtype',
            name='last_listening_time',
            field=models.DateTimeField(editable=False, null=True),
        ),
    ]
