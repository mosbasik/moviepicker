# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20150828_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchevent',
            name='group_organizing',
            field=models.OneToOneField(null=True, blank=True, to='main.WatchRoom'),
        ),
        migrations.AlterField(
            model_name='watchevent',
            name='user_present',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
