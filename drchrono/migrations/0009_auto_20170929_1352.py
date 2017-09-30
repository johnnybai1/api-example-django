# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0008_appointment_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='message',
            field=models.TextField(default=b'', max_length=500, blank=True),
        ),
    ]
