# Generated by Django 2.2.9 on 2020-01-13 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0004_auto_20200113_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='active',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]