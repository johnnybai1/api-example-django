# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0012_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentcheckin',
            name='appt_time',
            field=models.TimeField(default=datetime.time(14, 3, 40, 983981)),
            preserve_default=False,
        ),
    ]
