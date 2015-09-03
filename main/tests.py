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
# from unittest.TestCase import *


# class AnimalTestCase(TestCase):
#     def setUp(self):
#         Animal.objects.create(name="lion", sound="roar")
#         Animal.objects.create(name="cat", sound="meow")

#     def test_animals_can_speak(self):
#         """Animals that can speak are correctly identified"""
#         lion = Animal.objects.get(name="lion")
#         cat = Animal.objects.get(name="cat")
#         self.assertEqual(lion.speak(), 'The lion says "roar"')
#         self.assertEqual(cat.speak(), 'The cat says "meow"')


class MovieTestCase(TestCase):

    def setUp(self):

        # user setup
        user1 = User.objects.create(username='alice', email='alice@alice.com')
        user1.set_password('alice')

        # movie setup
        Movie.objects.create(imbd_id='tt0770828', title='Man of Steel')

    def test_movie_submission(self):
        '''Any user can add a movie to the database.'''

        # registered user case
        user_id = User.objects.get(username='alice').pk
        movie_1 = submit_movie(user_id_1, 'tt0468569')
        assert(Movie.object.filter(pk=movie_1.pk).exists())

        # anonymous user case
        movie_2 = submit_movie(None, 'tt0096895')
        assert(Movie.object.filter(pk=movie_2.pk).exists())

    def test_truncated_title_creation(self):
        '''Truncated title automatically created for newly submitted movie.'''

        movie = submit_movie(None, 'tt0468569')
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


class EventTestCase(TestCase):

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

        alpha_event = Event.objects.create(name='aplha',
                                           date_and_time="2015-09-19 21:30",
                                           description='fun event',
                                           group=alpha, creator=alice,
                                           location="basement")
        alpha_event.users.add(alice)
        alpha_event.users.add(bob)

    # An event must be associated with a group
    def test_event_group_parent(self):
        '''An event must be associated with a group'''
        user = User.objects.get(username='alice')

        test_event_1 = create_event('test1', "2015-09-19 21:30",
                                    'fun event', alpha, user, "basement")
        assert(test_event_1)

        test_event_2 = create_event('test2', "2015-10-19 21:30",
                                    'fun event', None, user, "basement")
        assert(not test_event_2)

    # An authenticated user can create an event
    # An anonymous user can't create an event
    def test_event_creation(self):
        '''Only authenticated users can create an event'''

        user = User.objects.get(username='alice')

        test_event_1 = create_event('test1', "2015-09-19 21:30",
                                    'fun event', alpha, user, "basement")
        assert(test_event_1)

        test_event_2 = create_event('test2', "2015-10-19 21:30",
                                    'fun event', alpha, None, "basement")
        assert(not test_event_2)

    # event IS_ACTIVE attribute can be toggled by the creator
    # event IS_ACTIVE attribute can't be toggled by other users
    def test_event_creator_toggle_active(self):
        '''Only the event creator can toggle the is_active property'''

        user_1 = User.objects.get(username='alice')
        user_2 = User.objects.get(username='bob')

        test_event_1 = create_event('test1', "2015-09-19 21:30",
                                    'fun event', alpha, user_1, "basement")
        deactivate_event(test_event_1, user_1)

        assert(test_event_1)

        test_event_2 = create_event('test2', "2015-10-19 21:30",
                                    'fun event', alpha, user_1, "basement")

        deactivate_event(test_event_2, user_2)

        assert(not test_event_2)

    # event IS_ACTIVE attribute = True - Users can join the event
    # event IS_ACTIVE attribute = False - Users can't join the event
    def test_event_active_join(self):
        '''Users can only join an event while the event is active'''
        user_1 = User.objects.get(username='alice')
        user_2 = User.objects.get(username='bob')
        user_3 = User.objects.get(username='eve')

        test_event_1 = create_event('test1', "2015-09-19 21:30",
                                    'fun event', alpha, user_1, "basement")
        test_event_1.users.add(user_2)

        assert(user_2 is in test_event_1.users.all())

        deactivate_event(test_event_1, user_1)
        test_event_1.users.add(user_3)

        assert(user_3 is not in test_event_1.users.all())

    # An authenticated group member can join an event
    # An authenticated non group member can join an event
    # An anonymous user can't join an event
    def test_event_join(self):
        '''Any authenticated user can join an event'''
        user_1 = User.objects.get(username='alice')
        user_2 = User.objects.get(username='bob')
        group_1 = Group.objects.get(name='alpha')

        group_1.users.add(user_1)

        test_event_1 = create_event('test1', "2015-09-19 21:30",
                                    'fun event', group_1, user_1, "basement")

        test_event_1.users.add(user_1)

        assert(user_1 is in test_event_1.users.all())

        test_event_1.users.add(user_2)

        assert(user_2 is in test_event_1.users.all())

        test_event_2 = create_event('test2', "2015-10-19 21:30",
                                    'a fun event', group_1, user_1, "my room")

        test_event_2.users.add(None)

        assert(test_event_2.users.all().count == 0)

    # Only movies that have been voted on by event member votes are
    #    brought into the event
    def test_event_movies(self):
        '''Only movies that have been voted on by event member votes are
        brought into the event'''
        trek_movies = Movies.objects.filter(title__icontains='trek')

        event = Event.objects.get(name='alpha_event')
        event_movies = get_event_movies(event.pk)

        assert(event_movies.count() == 2)
        event_movies = event_movies.distinct()
        assert(event_movies.count() == 2)
        for movie in event_movies:
            assert(movie in trek_movies)

    # Only the votes for the people who have joined the event are
    #   counted for the movies in an event
    def test_event_vote_count(self):
        '''Only event member votes are counted for the movie in the event'''
        event = Event.objects.get(name='alpha_event')
        event_movies = get_event_movies(event.pk)

        trek = event_movies.get(title='Star Trek')

        assert(trek.num_votes == 1)

    # Only the event creator can lock in or remove a movie from an event
    # Non-event creators can't lock in or remove a movie from an event
    def test_event_creator_lockin(self):
        '''Only the event creator should be able to lock in a movie'''

        event = Event.objects.get(name='alpha_event')
        event_creator = User.objects.get(username='alice')
        other_user = User.objects.get(username='bob')

        new_lockin = lockin_event(event.pk, event_creator)
        assert(new_lockin is in event.lockins.all())

        other_lockin = lockin_event(event.pk, other_user)
        assert(other_lockin is not in event.lockins.all())

    # When an event creator locks in a movie, a movie viewing is assigned to
    #   the members of that event
    def test_event_lockin_creates_viewings(self):
        '''Locking in an event creates a Viewing for all event members'''
        event_member = User.objects.get(username='alice')
        event = Event.objects.get(name='alpha_event')
        movie = event.movies.get(title='Star Trek')

        first_lockin = lockin_event(event.pk, movie.pk)

        assert(movie in event_member.viewings.all())

    # When a user joins an event, a movie viewing is assigned to them for every
    # movie already locked in to that event
    def test_event_join_creates_viewings(self):
        '''A viewing will be assigned to a user who joins a locked-in event'''
        late_event_member = User.objects.get(username='eve')
        event = Event.objects.get(name='alpha_event')
        movie = event.movies.get(title='Star Trek')

        first_lockin = lockin_event(event.pk, movie.pk)

        event.users.add(late_event_member)

        assert(movie in late_event_member.viewings.all())
