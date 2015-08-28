# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_auto_20150827_2224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchroom',
            old_name='created',
            new_name='created_time',
        ),
        migrations.AddField(
            model_name='watchroom',
            name='created_by',
            field=models.ForeignKey(related_name='creator', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
