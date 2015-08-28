# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150828_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchroom',
            name='created_by',
            field=models.ForeignKey(related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]