# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-29 04:31
from __future__ import unicode_literals

import api.models
import custom_storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0076_auto_20190720_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='map_image',
            field=models.FileField(blank=True, default=None, null=True, storage=custom_storages.LaunchImageStorage(), upload_to=api.models.location_path),
        ),
    ]
