# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-05 17:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_auto_20190103_1511'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spacestation',
            name='active_expedition',
        ),
        migrations.AddField(
            model_name='spacestation',
            name='active_expeditions',
            field=models.ManyToManyField(to='api.Expedition'),
        ),
        migrations.AlterField(
            model_name='expedition',
            name='space_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expeditions', to='api.SpaceStation'),
        ),
    ]
