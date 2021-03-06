# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-27 00:04
from __future__ import unicode_literals

import api.models
import custom_storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_astronauts_orbiter_orbiterflight_spacestation'),
    ]

    operations = [
        migrations.AddField(
            model_name='astronauts',
            name='profile_image',
            field=models.FileField(blank=True, default=None, null=True, storage=custom_storages.AstronautImageStorage(), upload_to=api.models.image_path),
        ),
        migrations.AddField(
            model_name='astronauts',
            name='wiki',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
