# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-04 22:15
from __future__ import unicode_literals

import uuid

from django.db import migrations, models


def seed_field(apps, schema_editor):
    infourls = apps.get_model('api', 'infourls')
    for m in infourls.objects.all():
        m.launch_id_migration = m.launch.launch_library_id
        m.save()

    vidurls = apps.get_model('api', 'vidurls')
    for m in vidurls.objects.all():
        m.launch_id_migration = m.launch.launch_library_id
        m.save()


class Migration(migrations.Migration):
    dependencies = [
        ('bot', '0004_remove_notification_launch'),
        ('api', '0021_launch_new_id_part2'),
    ]

    operations = [
        migrations.AddField(
            model_name='infourls',
            name='launch_id_migration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='vidurls',
            name='launch_id_migration',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(code=seed_field),
        migrations.RemoveField(
            model_name='infourls',
            name='launch',
        ),
        migrations.RemoveField(
            model_name='vidurls',
            name='launch',
        ),
        migrations.AlterField(
            model_name='launch',
            name='new_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='launch',
            name='launch_library_id',
            field=models.IntegerField(),
        ),
    ]
