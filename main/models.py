from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver


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
    # if "./manage.py migrate" breaks, try "./manage.py migrate --fake main,"
    # then run makemigrations and migrate again, which works.
    # I -- I just don't know.
    created_by = models.ForeignKey(User, unique=False, blank=True, null=True)

    def __unicode__(self):
        return self.title


@receiver(post_delete, sender=Movie)
def movie_post_delete_handler(sender, **kwargs):
    movie = kwargs['instance']
    storage, path = movie.poster.storage, movie.poster.path
    storage.delete(path)


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
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, unique=False, related_name='creator')

    def __unicode__(self):
        return self.name
