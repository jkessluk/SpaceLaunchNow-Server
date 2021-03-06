# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-09 05:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


def create_ids(apps, schema_editor):
    Mission = apps.get_model('api', 'mission')
    for m in Mission.objects.all():
        m.launch_library_id = m.id
        m.save()


def seed_field(apps, schema_editor):
    launch = apps.get_model('api', 'launch')
    for m in launch.objects.all():
        if m.mission is not None:
            m.mission_id_migration = m.mission.id
        m.save()


def rebuild_fk(apps, schema_editor):
    launch = apps.get_model('api', 'launch')
    mission = apps.get_model('api', 'mission')
    for m in launch.objects.all():
        if m.mission_id_migration is not None:
            mission = mission.objects.get(launch_library_id=m.mission_id_migration)
            if mission is not None:
                m.mission = mission
        m.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_mission_id_to_custom_id'),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='launch',
        #     name='mission_id_migration',
        #     field=models.IntegerField(default=0),
        # ),
        # migrations.RunPython(code=seed_field),
        migrations.RemoveField(
            model_name='launch',
            name='mission',
        ),
        migrations.RenameField(
            model_name='mission',
            old_name='id',
            new_name='launch_library_id',
        ),
        # migrations.AlterField(
        #     model_name='mission',
        #     name='launch_library_id',
        #     field=models.IntegerField(primary_key=False),
        # ),
        # migrations.AddField(
        #     model_name='mission',
        #     name='id',
        #     field=models.AutoField(primary_key=False)
        # ),
        # migrations.RunPython(code=create_ids),
        # migrations.AlterField(
        #     model_name='mission',
        #     name='id',
        #     field=models.AutoField(primary_key=True),
        # ),
        # migrations.AddField(
        #     model_name='launch',
        #     name='mission',
        #     field=models.ForeignKey(to='api.Mission',
        #                             null=True,
        #                             on_delete=models.SET_NULL),
        # ),
        # migrations.RunPython(code=rebuild_fk),
        # migrations.RemoveField(
        #     model_name='launch',
        #     name='mission_id_migration',
        # ),

    ]
