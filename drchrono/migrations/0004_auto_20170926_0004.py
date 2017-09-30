# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0003_auto_20170925_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='arrival_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
