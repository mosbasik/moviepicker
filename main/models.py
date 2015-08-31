from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    imdb_id = models.CharField(max_length=12, unique=True)
    title = models.CharField(max_length=255)
    truncated_title = models.CharField(max_length=255)
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
    submitter = models.ForeignKey(User, blank=True, null=True, related_name='movies_submitted')

    def __unicode__(self):
        return self.title


@receiver(post_delete, sender=Movie)
def movie_post_delete_handler(sender, **kwargs):
    movie = kwargs['instance']
    if movie.poster:
        storage, path = movie.poster.storage, movie.poster.path
        storage.delete(path)


class Group(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='movie_groups')
    creator = models.ForeignKey(User, related_name='groups_created')

    def __unicode__(self):
        return self.name


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    date_and_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    movies = models.ManyToManyField('Movie', through='Lockin', related_name='events')
    users = models.ManyToManyField(User, related_name='events')
    group = models.ForeignKey('Group', related_name='events')
    created_by = models.ForeignKey(User, related_name='events_created')
    location = models.ForeignKey('Location', null=True, blank=True, related_name='events')

    def __unicode__(self):
        return self.event_name


class Location(models.Model):

    LOCATION_TYPES = (
        (1, 'URL'),
        (2, 'Text'),
    )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    location_type = models.IntegerField(choices=LOCATION_TYPES)
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
    group = models.ForeignKey('Group', related_name='locations')

    @property
    def name(self):
        return self.url if self.url else self.text

    def __unicode__(self):
        return self.name


class Viewing(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='viewings')
    movie = models.ForeignKey('Movie', related_name='viewings')
    event = models.ForeignKey('Event', null=True, blank=True, related_name='viewings')
    date_and_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "{} - {} - {}".format(self.user,
                                     self.movie.title,
                                     self.date_and_time)


class LockIn(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey('Movie', related_name='lockins')
    event = models.ForeignKey('Event', related_name='lockins')

    def __unicode__(self):
        return "{} - {} - {}".format(self.event.name,
                                     self.movie.title,
                                     self.created)
