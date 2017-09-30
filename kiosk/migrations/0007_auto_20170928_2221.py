# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0006_auto_20170925_1707'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentCheckIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('time', models.TimeField(auto_now=True)),
                ('ssn', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='CheckIn',
        ),
        migrations.AlterField(
            model_name='demographics',
            name='address',
            field=models.CharField(default=b'blank', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='city',
            field=models.CharField(default=b'blank', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='emergency_contact_name',
            field=models.CharField(default=b'blank', max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='emergency_contact_phone',
            field=models.CharField(default=b'blank', max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='emergency_contact_relation',
            field=models.CharField(default=b'blank', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='ethnicity',
            field=models.CharField(default=b'blank', max_length=50, blank=True, choices=[(b'blank', b'None'), (b'hispanic', b'Hispanic or Latino'), (b'not_hispanic', b'Not Hispanic or Latino'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='gender',
            field=models.CharField(default=b'blank', max_length=10, blank=True, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'other', b'Other'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='race',
            field=models.CharField(default=b'blank', max_length=50, blank=True, choices=[(b'blank', b'None'), (b'indian', b'American Indian or Alaska Native'), (b'asian', b'Asian'), (b'black', b'Black or African American'), (b'white', b'White'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='demographics',
            name='zip_code',
            field=models.IntegerField(default=-1, blank=True),
        ),
        migrations.AlterField(
            model_name='reason',
            name='reason_for_visit',
            field=models.CharField(default=b'appt_checkin', max_length=30, choices=[(b'appt_checkin', b'I have an appointment.')]),
        ),
    ]
