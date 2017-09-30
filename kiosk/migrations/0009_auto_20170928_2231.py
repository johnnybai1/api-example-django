# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0008_auto_20170928_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentcheckin',
            name='appt_time',
            field=models.TimeField(help_text=b'Format: HH:MM'),
        ),
    ]
