# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-09 18:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_launcher_config_custom_part4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launcher',
            name='launcher_config',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='launcher', to='api.LauncherConfig'),
        ),
        migrations.AlterField(
            model_name='rocket',
            name='configuration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rocket', to='api.LauncherConfig'),
        ),
    ]
