# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-08-27 17:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgencyType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LandingLocation',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LandingType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LaunchStatus',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'verbose_name': 'Launch Status',
                'verbose_name_plural': 'Launch Statuses',
            },
        ),
        migrations.CreateModel(
            name='MissionType',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Orbit',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('abbrev', models.CharField(max_length=30)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Orbit',
                'verbose_name_plural': 'Orbits',
            },
        ),
    ]
