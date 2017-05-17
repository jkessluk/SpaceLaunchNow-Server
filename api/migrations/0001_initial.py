# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-17 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Launcher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('agency', models.CharField(default='Unknown', max_length=50)),
                ('imageURL', models.URLField(blank=True)),
                ('nationURL', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LauncherDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('agency', models.CharField(default='Unknown', max_length=50)),
                ('imageURL', models.URLField(blank=True)),
                ('nationURL', models.URLField(blank=True)),
                ('LVInfo', models.CharField(default='Unknown', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Orbiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('agency', models.CharField(default='Unknown', max_length=50)),
                ('history', models.CharField(default='', max_length=200)),
                ('details', models.CharField(default='', max_length=200)),
                ('imageURL', models.URLField(blank=True)),
                ('nationURL', models.URLField(blank=True)),
                ('wikiLink', models.URLField(blank=True)),
            ],
        ),
    ]
