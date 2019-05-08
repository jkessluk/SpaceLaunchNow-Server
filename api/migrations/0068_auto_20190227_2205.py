# Generated by Django 1.11.17 on 2019-03-04 21:28
from __future__ import unicode_literals

import api.models
import custom_storages
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0067_auto_20190202_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='expedition',
            field=models.ManyToManyField(blank=True, to='api.Expedition'),
        ),
        migrations.AddField(
            model_name='events',
            name='launch',
            field=models.ManyToManyField(blank=True, to='api.Launch'),
        ),
        migrations.AddField(
            model_name='events',
            name='spacestation',
            field=models.ManyToManyField(blank=True, to='api.SpaceStation'),
        ),
        migrations.AddField(
            model_name='events',
            name='video_url',
            field=models.URLField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='events',
            name='webcast_live',
            field=models.BooleanField(default=False),
        ),
    ]