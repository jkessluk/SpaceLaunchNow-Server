# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-05 02:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20181205_0238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agency',
            old_name='orbiters',
            new_name='spacecraft',
        ),
        migrations.RenameField(
            model_name='spacecraft',
            old_name='orbiter_config',
            new_name='spacecraft_config',
        ),
        migrations.AlterField(
            model_name='spacecraftconfiguration',
            name='launch_agency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='spacecraft_list', to='api.Agency'),
        ),
    ]
