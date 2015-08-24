# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('year', models.IntegerField(null=True, blank=True)),
                ('rating', models.FloatField(null=True, blank=True)),
                ('runtime', models.CharField(max_length=40, null=True, blank=True)),
                ('genre', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('starring', models.TextField(null=True, blank=True)),
                ('written_by', models.TextField(null=True, blank=True)),
                ('directed_by', models.CharField(max_length=255, null=True, blank=True)),
                ('poster', models.ImageField(null=True, upload_to=b'posters', blank=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('voters', models.ManyToManyField(related_name='votes', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WatchEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_name', models.CharField(max_length=255)),
                ('date_and_time', models.DateTimeField()),
                ('url_slug', models.SlugField(unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='WatchRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='watchevent',
            name='group_organizing',
            field=models.OneToOneField(to='main.WatchRoom'),
        ),
        migrations.AddField(
            model_name='watchevent',
            name='movie_watched',
            field=models.ForeignKey(to='main.Movie'),
        ),
        migrations.AddField(
            model_name='watchevent',
            name='user_present',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
