from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    imdb_id = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    imdb_rating = models.FloatField(null=True, blank=True)
    runtime = models.CharField(max_length=40, null=True, blank=True)
    genre = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    starring = models.TextField(null=True, blank=True)
    written_by = models.TextField(null=True, blank=True)
    directed_by = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='posters', null=True, blank=True)
    voters = models.ManyToManyField(User, related_name='votes', blank=True)
    user = models.ManyToManyField(User)

    def __unicode__(self):
        return self.title


class WatchEvent(models.Model):
    event_name = models.CharField(max_length=255)
    date_and_time = models.DateTimeField()
    url_slug = models.SlugField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True)
    movie_watched = models.ForeignKey('Movie')
    user_present = models.ForeignKey(User)
    group_organizing = models.OneToOneField('WatchRoom')

    def __unicode__(self):
        return self.event_name


class WatchRoom(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User)
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name