# django imports
from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Count

# local imports
from django.conf import settings

# external imports
from lxml import etree
from autoslug import AutoSlugField
import re
import requests
import StringIO
import urllib
import time


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
    # starring = models.TextField(null=True, blank=True)
    # written_by = models.TextField(null=True, blank=True)
    # directed_by = models.CharField(max_length=255, null=True, blank=True)
    poster = models.ImageField(upload_to='posters', null=True, blank=True)
    voters = models.ManyToManyField(User, related_name='votes')
    submitter = models.ForeignKey(User, blank=True, null=True, related_name='submitted_movies')
    watchers = models.ManyToManyField(User, through='Viewing', related_name='watched_movies')

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        no_articles = re.compile(r'(^a |^an |^the )', re.IGNORECASE)
        self.truncated_title = no_articles.sub('', self.title)
        super(Movie, self).save(*args, **kwargs)

    @staticmethod
    def create_vote(uid, imdb_id):
        '''
        Given a valid uid & valid IMDB id, adds the movie to the users' votes.
        Returns True on success and False on failure.
        '''
        if User.objects.filter(pk=uid).exists():
            if Movie.objects.filter(imdb_id=imdb_id).exists():
                user = User.objects.get(pk=uid)
                movie = Movie.objects.get(imdb_id=imdb_id)
                movie.voters.add(user)
                return True
        return False

    @staticmethod
    def delete_vote(uid, imdb_id):
        '''
        Given a valid uid & valid IMDB id, removes the movie from the users'
        votes. Returns True on success and False on failure.
        '''
        if User.objects.filter(pk=uid).exists():
            if Movie.objects.filter(imdb_id=imdb_id).exists():
                user = User.objects.get(pk=uid)
                movie = Movie.objects.get(imdb_id=imdb_id)
                movie.voters.remove(user)
                return True
        return False

    @staticmethod
    def submit_movie(uid, imdb_id):
        '''
        Given a user id (may contain None) and an IMDB id, returns a Movie
        object corresponding to that IMDB id.  Returns none if the IMDB id is
        malformed or not a movie.
        '''
        result = None

        if imdb_id is not None:

            # if the movie already exists locally, just retrieve the object
            # from our database and we're done
            if Movie.objects.filter(imdb_id=imdb_id).exists():
                result = Movie.objects.get(imdb_id=imdb_id)

            # if the movie doesn't already exist locally
            else:

                # save the TMDB api key for local use
                TMDB_KEY = settings.TMDB_KEY

                # Search TMDB with the IMDB ID
                t_payload = {'external_source': 'imdb_id', 'api_key': TMDB_KEY}
                t_url = 'https://api.themoviedb.org/3/find/%s'
                t_request = requests.get(t_url % imdb_id, params=t_payload)
                t_json = t_request.json()
                # print t_json

                # if that imdb_id is present in TMDB
                if t_json['movie_results']:

                    # Query TMDB with the newly-found TMDB ID
                    tmdb_id = t_json['movie_results'][0]['id']
                    t_payload = {'api_key': TMDB_KEY}
                    t_url = 'https://api.themoviedb.org/3/movie/%s'
                    t_request = requests.get(t_url % tmdb_id, params=t_payload)
                    t_json = t_request.json()

                    # create the movie object
                    movie = Movie()

                    # populate with guaranteed information
                    movie.submitter = None if uid is None else User.objects.get(pk=uid)
                    movie.imdb_id = imdb_id
                    movie.title = t_json['original_title']
                    movie.year = t_json['release_date'][:4]
                    movie.runtime = t_json['runtime']
                    movie.description = t_json['overview']
                    movie.imdb_rating = float(t_json['vote_average'])

                    # generate and store a string of genres
                    genre_string = ''
                    for genre in t_json['genres']:
                        genre_string += ', %s' % genre['name']
                    movie.genre = genre_string[2:]

                    # save the movie
                    movie.save()

                    # get the movie poster if it exists
                    movie.set_poster()

                    # queue the movie for return
                    result = movie

                    # delay for a half second to make sure we stay under TMDB's
                    # rate limit protocol (40 requests every 10 seconds)
                    time.sleep(.5)
        return result

    def set_poster(self):
        '''
        Scrapes the poster image from IMDB and stores it in the Movie's
        poster field.  If IMDB has no poster, nothing is stored.
        '''
        imdb_url = "http://www.imdb.com/title/%s/" % self.imdb_id
        result = urllib.urlopen(imdb_url)
        html = result.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(html), parser)
        poster_xpath = '//*[@id="img_primary"]/div[1]/a/img/@src'
        poster = tree.xpath(poster_xpath)

        # there's only ever one poster -- unless there isn't one.
        if len(poster) == 1:
            poster = poster[0]
            poster_response = urllib.urlopen(poster).read()
            poster_temp = NamedTemporaryFile(delete=True)
            poster_temp.write(poster_response)
            self.poster.save('%s.jpg' % self.title, File(poster_temp))


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
    slug = AutoSlugField(populate_from='name')
    description = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='movie_groups')
    creator = models.ForeignKey(User, related_name='groups_created')

    def __unicode__(self):
        return self.name

    @staticmethod
    def create_group(uid, name, description=None):
        '''
        Given a user id, a name string, and an optional description string,
        creates a new Group object.  If successful, returns the new group and a
        success message.  If unsuccessful, returns None and an error message.
        '''
        if User.objects.filter(pk=uid).exists():
            if not Group.objects.filter(name__iexact=name).exists():
                user = User.objects.get(pk=uid)
                group = Group()
                group.creator = user
                group.name = name
                if description is not None:
                    group.description = description
                group.save()
                group.join(uid)
                return group, 'Group "%s" created successfully.' % group.name
            return None, 'Group name already exists.'
        return None, 'Only registered users can create groups.'

    def join(self, uid):
        '''
        Given a user id, adds that user to the members of the group.  Returns
        True if successful, False if unsuccessful.
        '''
        if User.objects.filter(pk=uid).exists():
            self.users.add(User.objects.get(pk=uid))
            return True
        return False

    def leave(self, uid):
        '''
        Given a user id, remove that user from the members of the group.
        Returns True if successful, False if unsuccessful.
        '''
        if User.objects.filter(pk=uid).exists():
            self.users.remove(User.objects.get(pk=uid))
            return True
        return False

    def create_event(self, uid, name,
                     date_and_time=None, description=None, location=None):
        '''
        Given an authenticated user who is a group member, create an Event.
        Fails if the user is not authenticated or is not a member of the group.
        Return False if unsuccessful, return True if successful.
        '''
        if User.objects.filter(id=uid).exists():
            user = User.objects.get(id=uid)
            if user in self.users.all():
                event = Event.objects.create(
                    group=self, creator=user, name=name,
                    date_and_time=date_and_time, description=description,
                    location=location)
                return event
            return False
        return False

    def movie_pool(self):
        '''
        Returns the queryset of Movie objects for which this group's members
        have voted.  Each movie must include an annotation field "num_votes"
        containing the number of votes for that movie from group members.
        '''
        movies = Movie.objects.filter(
            voters__in=self.users.all()).annotate(num_votes=Count('voters'))
        return movies


class Event(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    date_and_time = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    watched_movies = models.ManyToManyField('Movie', through='LockIn', related_name='events')
    users = models.ManyToManyField(User, related_name='events')
    group = models.ForeignKey('Group', related_name='events')
    creator = models.ForeignKey(User, related_name='events_created')
    location = models.ForeignKey('Location', null=True, blank=True, related_name='events')
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    def join(self, uid):
        '''
        Given any valid user id from the site, adds that user to the members of
        the group. Fails on invalid user id. The event must be active for users
        to be able to join the event.  Returns True if successful; False
        if unsuccessful.
        '''
        if User.objects.filter(id=uid).exists():
            if self.is_active is True:
                user = User.objects.get(pk=uid)
                lockins = LockIn.objects.filter(event=self)
                for lockin in lockins:
                    Viewing.objects.get_or_create(
                        user=user,
                        event=self,
                        movie=lockin.movie,
                        date_and_time=lockin.created,
                    )
                self.users.add(user)
                return True
        return False

    def leave(self, uid):
        '''
        Given any valid user id from the site, removes that user from the
        members of the group. Fails on invalid user id.  Returns True if
        successful; False if unsuccessful.
        '''
        if User.objects.filter(id=uid).exists():
            self.users.remove(User.objects.get(id=uid))
            return True
        return False

    def activate(self, uid):
        '''
        Given the user id of the event's creator, sets is_active to True on the
        event. Fails if the user id is not the event's creator.  Returns True
        if successful; False if unsuccessful.
        '''
        if self.creator.id == uid:
            self.is_active = True
            return True
        return False

    def deactivate(self, uid):
        '''
        Given the user id of the event's creator, sets is_active to False on
        the event. Fails if the user id is not the event's creator.  Returns
        True if successful; False if unsuccessful.
        '''
        if self.creator.id == uid:
            self.is_active = False
            return True
        return False

    def movie_pool(self):
        '''
        Returns the queryset of Movie objects for which this event's members
        have voted.  Each movie must include an annotation field "num_votes"
        containing the number of votes for that movie from event members.
        '''
        movies = Movie.objects.filter(
            voters__in=self.users.all()).annotate(
            num_votes=Count('voters')).order_by('-num_votes')
        return movies

    def lockin(self, uid, imdb_id):
        '''
        Given the user id of the event's creator and a valid imdb_id, adds that
        movie to the the event's watched movies (via the LockIn model) and adds
        it to all event members' watched movies (via the Viewing model). Fails
        if the user is invalid, the user is not the creator, or the imdb_id is
        invalid. Returns True if successful; False if unsuccessful.
        '''
        if User.objects.filter(pk=uid).exists():
            user = User.objects.get(pk=uid)
            if user == self.creator:
                if Movie.objects.filter(imdb_id=imdb_id).exists():
                    movie = Movie.objects.get(imdb_id=imdb_id)
                    lockin = LockIn.objects.create(event=self, movie=movie)
                    event_members = self.users.all()
                    for event_member in event_members:
                        Viewing.create(
                            uid=event_member.pk,
                            imdb_id=imdb_id,
                            event_id=self.pk,
                        )
                    return True
        return False

    def lockin_remove(self, uid, imdb_id):
        '''
        Given the user id of the event's creator and a valid imdb_id, removes
        that movie from the the event's watched movies (via the LockIn model)
        and removes it from all event members' watched movies (via the Viewing
        model). Fails if the user is invalid, the user is not the creator, or
        the imdb_id is invalid. Returns True if successful; False if
        unsuccessful.
        '''
        if User.objects.filter(pk=uid).exists():
            user = User.objects.get(pk=uid)
            if user == self.creator:
                if self.watched_movies.filter(imdb_id=imdb_id).exists():
                    movie = Movie.objects.get(imdb_id=imdb_id)
                    LockIn.objects.filter(event=self, movie=movie).delete()
                    event_members = self.users.all()
                    for event_member in event_members:
                        Viewing.objects.filter(
                            user=event_member,
                            event=self,
                            movie=movie,
                        ).delete()
                    return True
        return False


class Location(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    text = models.TextField(null=True, blank=True)
    group = models.ForeignKey('Group', related_name='locations')

    def __unicode__(self):
        return self.text


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

    @staticmethod
    def create(uid, imdb_id, event_id=None):
        '''
        Given a user id, an imdb id and optionally an event_id; creates a
        Viewing object and removes that movie from that user's set of votes.
        Fails if the user or movie id is invalid. Returns the new Viewing if
        successful; returns None if unsuccessful.
        '''
        if User.objects.filter(pk=uid).exists():
            if Movie.objects.filter(imdb_id=imdb_id).exists():
                movie = Movie.objects.get(imdb_id=imdb_id)
                user = User.objects.get(pk=uid)
                viewing = Viewing()
                viewing.user = user
                viewing.movie = movie
                if Event.objects.filter(pk=event_id).exists():
                    viewing.event = Event.objects.get(pk=event_id)
                viewing.save()
                Movie.delete_vote(user.pk, movie.imdb_id)
        return None


class LockIn(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey('Movie', related_name='lockins')
    event = models.ForeignKey('Event', related_name='lockins')

    def __unicode__(self):
        return "{} - {} - {}".format(self.event.name,
                                     self.movie.title,
                                     self.created)
