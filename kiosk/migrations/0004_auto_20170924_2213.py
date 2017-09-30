# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0003_auto_20170924_1745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personaldetails',
            old_name='mail_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='personaldetails',
            old_name='emergency_name',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='personaldetails',
            old_name='emergency_phone',
            new_name='emergency_contact_phone',
        ),
        migrations.RenameField(
            model_name='personaldetails',
            old_name='emergency_relation',
            new_name='emergency_contact_relation',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='home_city',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='home_zip',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='mail_city',
        ),
        migrations.RemoveField(
            model_name='personaldetails',
            name='mail_zip',
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='emergency_contact_name',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='zip_code',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ethnicity',
            name='ethnicity',
            field=models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'hispanic', b'Hispanic or Latino'), (b'not_hispanic', b'Not Hispanic or Latino'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='gender',
            name='gender',
            field=models.CharField(default=b'declined', max_length=30, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'Other', b'Other'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='race',
            name='race',
            field=models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'indian', b'American Indian or Alaska Native'), (b'asian', b'Asian'), (b'black', b'Black or African American'), (b'white', b'White'), (b'decline', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='reason',
            name='reason_for_visit',
            field=models.CharField(default=b'APPT', max_length=30, choices=[(b'APPT', b'I have an appointment.'), (b'BLANK', b'No reason')]),
        ),
    ]
