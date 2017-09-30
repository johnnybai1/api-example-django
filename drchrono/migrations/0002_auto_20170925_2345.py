# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='arrival_time',
            field=models.TimeField(default=datetime.datetime(2017, 9, 26, 6, 44, 59, 142421, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='first_name',
            field=models.CharField(default='hello', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='appointment',
            name='last_name',
            field=models.CharField(default='hello', max_length=30),
            preserve_default=False,
        ),
    ]
