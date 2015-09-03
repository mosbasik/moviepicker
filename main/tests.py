# django imports
from django.test import TestCase
from django.contrib.auth.models import User

# local imports
from main.models import (
    Movie,
    Group,
    Event,
    Location,
    Viewing,
    LockIn,
)

# python imports
from unittest import skip


class MovieTestCase(TestCase):

    def setUp(self):

        # user setup
        user1 = User.objects.create(username='alice', email='alice@alice.com')
        user1.set_password('alice')

        # movie setup
        Movie.objects.create(imdb_id='tt0770828', title='Man of Steel')

    def test_movie_submission(self):
        '''Any user can add a movie to the database.'''

        # registered user case
        alice = User.objects.get(username='alice')
        movie_1 = Movie.submit_movie(alice.pk, 'tt0468569')
        assert(Movie.objects.filter(pk=movie_1.pk).exists())

        # anonymous user case
        movie_2 = Movie.submit_movie(None, 'tt0096895')
        assert(Movie.objects.filter(pk=movie_2.pk).exists())

    def test_truncated_title_creation(self):
        '''Truncated title automatically created for newly submitted movie.'''

        movie = Movie.submit_movie(None, 'tt0468569')
        assert(movie.truncated_title)

    # An authenticated user can vote for a movie
    # An anonymous user can't vote for a movie
    def test_movie_voting(self):

        # registered user case
        user = User.objects.get(username='alice')
        user_id = user.pk

        movie = Movie.objects.get(imdb_id='tt0770828')
        imdb_id = movie.imdb_id

        vote_succeeded = vote_for_movie(user_id, imdb_id)

        assert(vote_succeeded)
        assert(movie in user.votes.all())

        # anonymous user case
        user_id = None
        movie = Movie.objects.get(imdb_id='tt0770828')
        imdb_id = movie.imdb_id

        vote_succeeded = vote_for_movie(user_id, imdb_id)

        assert(not vote_succeeded)


@skip
class GroupTestCase(TestCase):

    def setUp(self):

        # user setup
        alice = User.objects.create(username='alice')
        bob = User.objects.create(username='bob')
        eve = User.objects.create(username='eve')

        # movie setup
        trek_into_darkness = Movie.objects.create(
            imbdb_id='tt1408101',
            title='Star Trek Into Darkness')
        trek = Movie.objects.create(
            imbdb_id='tt0796366',
            title='Star Trek')
        star_wars = Movie.objects.create(
            imbdb_id='tt0076759',
            title='Star Wars: Episode IV - A New Hope')

        # vote setup
        alice.votes.add(trek_into_darkness)
        bob.votes.add(trek)
        eve.votes.add(star_wars)
        eve.votes.add(trek)

        # group setup
        alpha = Group.objects.create(name='Alpha', creator=alice)
        alpha.users.add(alice)
        alpha.users.add(bob)

    # An authenticated user can create a group
    # An anonymous user can't create a group
    def test_group_creation(self):

        # registered user case
        user = User.objects.get(username='alice')
        user_id = user.pk

        group_2 = create_group(user_id, 'Bravo', description='second group')
        assert(Group.objects.filter(pk=group_2.pk).exists())
        assert(user == group_2.creator)

        group_3 = create_group(user_id, 'Charlie')
        assert(Group.objects.filter(pk=group_3.pk).exists())
        assert(user == group_3.creator)

        # anonymous user case
        user_id = None

        group_4 = create_group(user_id, 'Delta')

        assert(group_4 is None)

    # An authenticated user can join a group
    # An anonymous user can't join a group
    def test_group_joining(self):

        # registered user case
        user = User.objects.get(username='alice')
        user_id = user.pk

        group = Group.objects.get(name='Alpha')
        group_id

        join_succeeded = join_group(user_id, group_id)

        assert(join_succeeded)
        assert(user in group.users.all())

        # anonymous user case
        user_id = None

        group = Group.objects.get(name='Alpha')
        group_id = group.pk

        join_succeeded = join_group(user_id, group_id)

        assert(not join_succeeded)

    # Specifically the movies that members of a groups have voted for
    #   are shown in the group
    def test_group_movie_list(self):
        trek_movies = Movies.objects.filter(title__icontains='trek')

        group = Group.objects.get(name='Alpha')
        group_movies = get_group_movies(group.pk)

        assert(group_movies.count() == 2)
        group_movies = group_movies.distinct()
        assert(group_movies.count() == 2)
        for movie in group_movies:
            assert(movie in trek_movies)

    # Only the votes for movies of members of a group are counted within the
    #   group
    def test_group_vote_count(self):
        group = Group.objects.get(name='Alpha')
        group_movies = get_group_movies(group.pk)

        trek = group_movies.get(title='Star Trek')

        assert(trek.num_votes == 1)


@skip
class EventTestCase(TestCase):

    def setUp(self):
        assert(False)

    # An event must be associated with a group
    def test_event_group_parent(self):
        assert(False)

    # An authenticated user can create an event
    # An anonymous user can't create an event
    def test_event_creation(self):
        assert(False)

    # event IS_ACTIVE attribute can be toggled by the creator
    # event IS_ACTIVE attribute can't be toggled by other users
    def test_event_creator_toggle_active(self):
        assert(False)

    # event IS_ACTIVE attribute = True - Users can join the event
    # event IS_ACTIVE attribute = False - Users can't join the event
    def test_event_active_join(self):
        assert(False)

    # An authenticated group member can join an event
    # An authenticated non group member can join an event
    # An anonymous user can't join an event
    def test_event_join(self):
        assert(False)

    # Only the votes for the people who have joined the event are
    #   counted for the movies in an event
    def test_event_vote_count(self):
        assert(False)

    # Only the event creator can lock in or remove a movie from an event
    # Non-event creators can't lock in or remove a movie from an event
    def test_event_creator_lockin(self):
        assert(False)

    # When an event creator locks in a movie, a movie viewing is assigned to
    #   the members of that event
    def test_event_lockin_creates_views(self):
        assert(False)

    # When a user joins an event, a movie viewing is assigned to them for every
    # movie already locked in to that event
    def test_event_join_creates_views(self):
        assert(False)
