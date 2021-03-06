# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-03 20:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0052_auto_20181220_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='spacestation',
            name='active_expedition',
            field=models.ManyToManyField(blank=True, null=True, to='api.Expedition'),
        ),
        migrations.AlterField(
            model_name='spacecraftflight',
            name='spacecraft',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spacecraftflight', to='api.Spacecraft'),
        ),
        migrations.AlterField(
            model_name='spacestation',
            name='orbit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurations.Orbit'),
        ),
    ]
