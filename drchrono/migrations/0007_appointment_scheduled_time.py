# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0006_delete_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='scheduled_time',
            field=models.TimeField(null=True, blank=True),
        ),
    ]
