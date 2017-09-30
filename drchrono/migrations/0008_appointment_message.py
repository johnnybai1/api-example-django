# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0007_appointment_scheduled_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='message',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
