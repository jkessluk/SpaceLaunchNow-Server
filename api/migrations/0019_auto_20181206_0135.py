# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-06 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0007_astronautrole'),
        ('api', '0018_auto_20181205_0140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='astronautflight',
            name='tag',
        ),
        migrations.AddField(
            model_name='astronautflight',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configurations.AstronautRole'),
        ),
    ]
