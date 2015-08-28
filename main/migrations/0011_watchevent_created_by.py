# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_auto_20150828_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchevent',
            name='created_by',
            field=models.ForeignKey(related_name='event_creator', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
