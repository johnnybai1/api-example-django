# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0002_auto_20170924_0509'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('ssn', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ethnicity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ethnicity', models.CharField(default=b'N', max_length=50, choices=[(b'H_L', b'Hispanic or Latino'), (b'NOT', b'Not Hispanic or Latino'), (b'N', b'Declined to specify')])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField()),
                ('home_address', models.CharField(max_length=200)),
                ('home_zip', models.PositiveIntegerField()),
                ('home_city', models.CharField(max_length=100)),
                ('mail_address', models.CharField(max_length=200, blank=True)),
                ('mail_zip', models.PositiveIntegerField(blank=True)),
                ('mail_city', models.CharField(max_length=200, blank=True)),
                ('emergency_name', models.CharField(max_length=100, blank=True)),
                ('emergency_phone', models.CharField(max_length=20, blank=True)),
                ('emergency_relation', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('race', models.CharField(default=b'N', max_length=50, choices=[(b'AI_AN', b'American Indian or Alaska Native'), (b'H_L', b'Hispanic or Latino'), (b'A', b'Asian'), (b'AA', b'Black or African American'), (b'W', b'White'), (b'N', b'Declined to specify')])),
            ],
        ),
        migrations.AlterField(
            model_name='gender',
            name='gender',
            field=models.CharField(default=b'N', max_length=30, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other'), (b'N', b'Declined to specify')]),
        ),
    ]
