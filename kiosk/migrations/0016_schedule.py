# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0015_auto_20170929_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=5)),
                ('date_of_birth', models.CharField(help_text=b'yyyy-mm-dd', max_length=10)),
                ('time', models.CharField(help_text=b'HH:MM AM/PM', max_length=10)),
            ],
        ),
    ]
