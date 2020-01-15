# Generated by Django 2.2.9 on 2020-01-15 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publisher',
            name='category',
            field=models.SmallIntegerField(choices=[(1, 'Programmatic'), (2, 'Managed'), (999, 'System'), (-1, 'Testing'), (-2, 'Unitesting')], default=2),
        ),
    ]
