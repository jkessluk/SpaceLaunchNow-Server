# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-13 23:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurations', '0007_astronautrole'),
    ]

    operations = [
        migrations.CreateModel(
            name='DockingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Docking Location',
                'verbose_name_plural': 'Docking Locations',
            },
        ),
    ]
