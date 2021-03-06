# Generated by Django 2.2.9 on 2020-01-16 01:39

import console.models
from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, editable=False)),
                ('source', models.CharField(editable=False, max_length=128)),
                ('publish_time', models.DateTimeField(auto_now_add=True)),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(editable=False)),
            ],
            options={
                'db_table': 'event',
            },
            bases=(console.models.ModelEventMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EventProcessingModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('active_modified', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=64)),
                ('code', models.TextField(null=True)),
                ('parameters', models.TextField(null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('active_modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'event_processing_module',
            },
        ),
        migrations.CreateModel(
            name='EventType',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('active_modified', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('category', models.SmallIntegerField(choices=[(1, 'Programmatic'), (2, 'Managed'), (999, 'System'), (-1, 'Testing'), (-2, 'Unitesting')], default=2)),
                ('comments', models.TextField(blank=True, null=True)),
                ('sample', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('active_modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'event_type',
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('active_modified', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('category', models.SmallIntegerField(choices=[(1, 'Programmatic'), (2, 'Managed'), (999, 'System'), (-1, 'Testing'), (-2, 'Unitesting')], default=2)),
                ('comments', models.TextField(null=True)),
                ('active_modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'publisher',
            },
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('active_modified', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('category', models.SmallIntegerField(choices=[(1, 'Programmatic'), (2, 'Managed'), (999, 'System'), (-1, 'Testing'), (-2, 'Unitesting')], default=2)),
                ('comments', models.TextField(blank=True, null=True)),
                ('active_modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'subscriber',
            },
        ),
        migrations.CreateModel(
            name='SubscribedEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_host', models.CharField(editable=False, max_length=256)),
                ('process_pid', models.CharField(editable=False, max_length=32, null=True)),
                ('process_times', models.IntegerField(default=1, editable=False)),
                ('process_start_time', models.DateTimeField(auto_now_add=True)),
                ('process_end_time', models.DateTimeField(editable=False, null=True)),
                ('status', models.IntegerField(default=0, editable=False)),
                ('result', models.TextField(editable=False, null=True)),
                ('event', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='subscribed', to='console.Event')),
                ('event_type', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='subscribed_events', to='console.EventType')),
                ('publisher', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='subscribed_publisher_events', to='console.Publisher')),
                ('subscriber', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='console.Subscriber')),
            ],
            options={
                'index_together': {('event',), ('publisher', 'event_type', 'status')},
                'unique_together': {('subscriber', 'publisher', 'event_type', 'event')},
                'db_table': 'subscribed_event',
            },
        ),
        migrations.AddField(
            model_name='eventtype',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_types', to='console.Publisher'),
        ),
        migrations.CreateModel(
            name='EventProcessingHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_host', models.CharField(editable=False, max_length=256)),
                ('process_pid', models.CharField(editable=False, max_length=32, null=True)),
                ('process_start_time', models.DateTimeField(editable=False)),
                ('process_end_time', models.DateTimeField(editable=False, null=True)),
                ('status', models.IntegerField(editable=False)),
                ('result', models.TextField(editable=False, null=True)),
                ('subscribed_event', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='processing_history', to='console.SubscribedEvent')),
            ],
            options={
                'db_table': 'event_processing_history',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='events', to='console.EventType'),
        ),
        migrations.AddField(
            model_name='event',
            name='publisher',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='publisher_events', to='console.Publisher'),
        ),
        migrations.CreateModel(
            name='SubscribedEventType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True, editable=False)),
                ('active_modified', models.DateTimeField(editable=False, null=True)),
                ('category', models.SmallIntegerField(choices=[(1, 'Programmatic'), (2, 'Managed'), (999, 'System'), (-1, 'Testing'), (-2, 'Unitesting')], default=2)),
                ('parameters', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('last_dispatched_time', models.DateTimeField(editable=False, null=True)),
                ('active_modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('event_processing_module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='console.EventProcessingModule')),
                ('event_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscribed_event_types', to='console.EventType')),
                ('last_dispatched_event', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='console.Event')),
                ('modifier', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('publisher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscribed_publisher_event_types', to='console.Publisher')),
                ('subscriber', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='event_types', to='console.Subscriber')),
            ],
            options={
                'unique_together': {('subscriber', 'publisher', 'event_type')},
                'db_table': 'subscribed_event_type',
            },
        ),
        migrations.AlterUniqueTogether(
            name='eventtype',
            unique_together={('publisher', 'name')},
        ),
        migrations.AlterIndexTogether(
            name='event',
            index_together={('publisher', 'event_type'), ('publisher',)},
        ),
    ]
