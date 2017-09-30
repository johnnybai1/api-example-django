# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0002_auto_20170925_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='arrival_time',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='checkin_time',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='finish_time',
            field=models.TimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='seen_time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
