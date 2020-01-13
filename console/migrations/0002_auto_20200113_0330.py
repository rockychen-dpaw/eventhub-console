# Generated by Django 2.2.9 on 2020-01-13 03:30

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publisher',
            name='managed',
        ),
        migrations.AddField(
            model_name='subscriber',
            name='active',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='console.EventType'),
        ),
        migrations.AlterField(
            model_name='event',
            name='payload',
            field=django.contrib.postgres.fields.jsonb.JSONField(editable=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='publisher',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='publisher_events', to='console.Publisher'),
        ),
        migrations.AlterField(
            model_name='event',
            name='source',
            field=models.CharField(editable=False, max_length=128),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='comments',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='managed',
            field=models.BooleanField(default=True, editable=False),
        ),
        migrations.AlterField(
            model_name='eventtype',
            name='sample',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]