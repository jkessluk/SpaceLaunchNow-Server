# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-12-05 06:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0005_astronautstatus_orbiterstatus_spacestationstatus'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrbiterStatus',
            new_name='SpacecraftStatus',
        ),
        migrations.AlterModelOptions(
            name='spacecraftstatus',
            options={'verbose_name': 'Spacecraft Status', 'verbose_name_plural': "Spacecraft Status'"},
        ),
    ]