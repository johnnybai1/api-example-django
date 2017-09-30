# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0013_appointmentcheckin_appt_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentcheckin',
            name='appt_time',
            field=models.CharField(max_length=10),
        ),
    ]
