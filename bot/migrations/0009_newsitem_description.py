# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-04-29 19:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0008_auto_20190428_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsitem',
            name='description',
            field=models.CharField(blank=True, default='', max_length=40000, null=True),
        ),
    ]
