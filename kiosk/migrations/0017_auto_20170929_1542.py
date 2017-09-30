# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0016_schedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='time',
            field=models.CharField(help_text=b'HH:MM AM/PM', max_length=10, verbose_name=b'Appointment Time'),
        ),
    ]
