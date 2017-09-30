# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0010_auto_20170928_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentcheckin',
            name='appt_time',
        ),
    ]
