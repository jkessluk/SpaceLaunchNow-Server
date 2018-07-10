# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-07-10 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_auto_20180708_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='launcher',
            name='capability',
        ),
        migrations.RemoveField(
            model_name='launcher',
            name='in_use',
        ),
        migrations.AddField(
            model_name='launcher',
            name='reusable',
            field=models.BooleanField(default=False),
        ),
    ]