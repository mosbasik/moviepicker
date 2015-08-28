# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20150828_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchevent',
            name='url_slug',
            field=models.SlugField(),
        ),
    ]
