# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20150826_2314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='created_by',
        ),
        migrations.AddField(
            model_name='movie',
            name='created_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
