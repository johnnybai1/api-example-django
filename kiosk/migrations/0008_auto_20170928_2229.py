# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0007_auto_20170928_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointmentcheckin',
            old_name='time',
            new_name='appt_time',
        ),
    ]
