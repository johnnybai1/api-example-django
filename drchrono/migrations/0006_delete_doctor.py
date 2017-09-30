# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0005_auto_20170926_0011'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Doctor',
        ),
    ]
