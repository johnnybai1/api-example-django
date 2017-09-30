# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0004_auto_20170924_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='Demographics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.CharField(default=b'blank', max_length=10)),
                ('address', models.CharField(default=b'blank', max_length=200)),
                ('zip_code', models.IntegerField(default=b'blank')),
                ('city', models.CharField(default=b'blank', max_length=100)),
                ('emergency_contact_name', models.CharField(default=b'blank', max_length=100)),
                ('emergency_contact_phone', models.CharField(default=b'blank', max_length=20)),
                ('emergency_contact_relation', models.CharField(default=b'blank', max_length=50)),
                ('gender', models.CharField(default=b'blank', max_length=10, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'other', b'Other'), (b'declined', b'Declined to specify')])),
                ('race', models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'indian', b'American Indian or Alaska Native'), (b'asian', b'Asian'), (b'black', b'Black or African American'), (b'white', b'White'), (b'declined', b'Declined to specify')])),
                ('ethnicity', models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'hispanic', b'Hispanic or Latino'), (b'not_hispanic', b'Not Hispanic or Latino'), (b'declined', b'Declined to specify')])),
            ],
        ),
        migrations.AddField(
            model_name='gender',
            name='ethnicity',
            field=models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'hispanic', b'Hispanic or Latino'), (b'not_hispanic', b'Not Hispanic or Latino'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AddField(
            model_name='gender',
            name='race',
            field=models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'indian', b'American Indian or Alaska Native'), (b'asian', b'Asian'), (b'black', b'Black or African American'), (b'white', b'White'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AddField(
            model_name='personaldetails',
            name='gender',
            field=models.CharField(default=b'declined', max_length=30, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'other', b'Other'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='ssn',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='gender',
            name='gender',
            field=models.CharField(default=b'declined', max_length=30, choices=[(b'Male', b'Male'), (b'Female', b'Female'), (b'other', b'Other'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='personaldetails',
            name='date_of_birth',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='race',
            name='race',
            field=models.CharField(default=b'blank', max_length=50, choices=[(b'blank', b'None'), (b'indian', b'American Indian or Alaska Native'), (b'asian', b'Asian'), (b'black', b'Black or African American'), (b'white', b'White'), (b'declined', b'Declined to specify')]),
        ),
        migrations.AlterField(
            model_name='reason',
            name='reason_for_visit',
            field=models.CharField(default=b'APPT', max_length=30, choices=[(b'APPT', b'I have an appointment.')]),
        ),
    ]
