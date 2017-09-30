# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0004_auto_20170926_0004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='arrival_time',
        ),
        migrations.AddField(
            model_name='appointment',
            name='checkin_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
