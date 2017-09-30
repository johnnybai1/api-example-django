# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('day_of_week', models.CharField(max_length=9)),
                ('waited_for', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='appointmentstatus',
            name='status',
            field=models.CharField(default=b'', max_length=20, choices=[(b'', b''), (b'Arrived', b'Arrived'), (b'Cancelled', b'Cancelled'), (b'Checked In', b'Checked In'), (b'Complete', b'Complete'), (b'Confirmed', b'Confirmed'), (b'In Session', b'In Session'), (b'No Show', b'No Show'), (b'Not Confirmed', b'Not Confirmed'), (b'Rescheduled', b'Rescheduled')]),
        ),
    ]
