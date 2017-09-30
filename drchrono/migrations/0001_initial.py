# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('checkin_time', models.TimeField(blank=True)),
                ('seen_time', models.TimeField(blank=True)),
                ('finish_time', models.TimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.CharField(max_length=30, serialize=False, primary_key=True)),
            ],
        ),
    ]
