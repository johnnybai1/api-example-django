# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_auto_20170925_1915'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('checkin_time', models.CharField(max_length=20)),
                ('wait_time', models.CharField(max_length=8)),
                ('reason', models.CharField(max_length=100)),
                ('message', models.TextField(default=b'', max_length=500, blank=True)),
            ],
        ),
    ]
