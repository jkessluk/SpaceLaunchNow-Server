# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-11 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_dailydigestrecord_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='launch',
            name='img_url',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
