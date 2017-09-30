# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0005_auto_20170925_0921'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ethnicity',
        ),
        migrations.DeleteModel(
            name='Gender',
        ),
        migrations.DeleteModel(
            name='PersonalDetails',
        ),
        migrations.DeleteModel(
            name='Race',
        ),
        migrations.AlterField(
            model_name='demographics',
            name='zip_code',
            field=models.IntegerField(default=-1),
        ),
    ]
