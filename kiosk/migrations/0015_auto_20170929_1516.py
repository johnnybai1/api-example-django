# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0014_auto_20170929_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentcheckin',
            name='appt_time',
            field=models.CharField(help_text=b'hh:mm AM/PM', max_length=10),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='date_of_birth',
            field=models.CharField(default=b'blank', help_text=b'yyyy-mm-dd', max_length=10),
        ),
        migrations.AlterField(
            model_name='reason',
            name='reason_for_visit',
            field=models.CharField(default=b'appt_checkin', max_length=30, choices=[(b'appt_checkin', b'I have an appointment'), (b'appt_schedule', b'I want to schedule an appointment')]),
        ),
    ]
