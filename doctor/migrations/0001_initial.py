# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'', max_length=20, choices=[(b'', b''), (b'Arrived', b'Arrived'), (b'Cancelled', b'Cancelled'), (b'Complete', b'Complete'), (b'Confirmed', b'Confirmed'), (b'In Session', b'In Session'), (b'No Show', b'No Show'), (b'Not Confirmed', b'Not Confirmed'), (b'Rescheduled', b'Rescheduled')])),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
    ]
