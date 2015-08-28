# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_watchevent_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchevent',
            name='movie_watched',
            field=models.ForeignKey(blank=True, to='main.Movie', null=True),
        ),
    ]
