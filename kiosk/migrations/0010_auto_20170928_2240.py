# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0009_auto_20170928_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentcheckin',
            name='appt_time',
            field=models.TimeField(help_text=b'HH:MM AM or PM'),
        ),
    ]
