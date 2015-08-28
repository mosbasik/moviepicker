# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150828_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchroom',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
