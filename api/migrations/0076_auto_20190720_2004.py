# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-21 00:04
from __future__ import unicode_literals

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0075_auto_20190718_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='launch',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from=['name', 'hashtag', 'id']),
        ),
    ]
