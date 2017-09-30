# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(default=b'N', max_length=30, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other'), (b'N', b'Decline to specify')])),
            ],
        ),
        migrations.AlterField(
            model_name='reason',
            name='reason_for_visit',
            field=models.CharField(default=b'APPT', max_length=30, choices=[(b'APPT', b'I have an appointment.'), (b'NONE', b'No reason')]),
        ),
    ]
