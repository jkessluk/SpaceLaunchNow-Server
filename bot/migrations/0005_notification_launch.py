# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-09 04:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def rebuild_fk(apps, schema_editor):
    notification = apps.get_model('bot', 'notification')
    LaunchModel = apps.get_model('api', 'launch')
    for m in notification.objects.all():
        launch = LaunchModel.objects.get(launch_library_id=m.launch_id_migration)
        m.launch = launch
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20181208_2300'),
        ('bot', '0004_remove_notification_launch'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='launch',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Launch'),
        ),
        migrations.RunPython(code=rebuild_fk),
        migrations.RemoveField(
            model_name='notification',
            name='launch_id_migration',
        ),
    ]
