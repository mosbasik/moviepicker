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
        alice = User.objects.create(username='alice')

        # movie setup
        mos = Movie.objects.create(imdb_id='tt0770828', title='Man of Steel')
        superman = Movie.objects.create(imdb_id='tt0078346', title='Superman')

        # vote setup
        alice.votes.add(superman)

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

    def test_movie_create_vote(self):
        '''Authed users can create votes for a movie; anonymous users can't.'''

        # registered user case
        alice = User.objects.get(username='alice')
        man_of_steel = Movie.objects.get(title='Man of Steel')
        assert(man_of_steel not in alice.votes.all())
        create_succesful = Movie.create_vote(alice.pk, man_of_steel.imdb_id)
        assert(create_succesful)
        assert(man_of_steel in alice.votes.all())

        # anonymous user case
        man_of_steel = Movie.objects.get(title='Man of Steel')
        create_succesful = Movie.create_vote(None, man_of_steel.imdb_id)
        assert(not create_succesful)

    def test_movie_delete_vote(self):
        '''Authed users can delete votes for a movie; anonymous users can't.'''

        # registered user case
        alice = User.objects.get(username='alice')
        superman = Movie.objects.get(title='Superman')
        assert(superman in alice.votes.all())
        delete_successful = Movie.delete_vote(alice.pk, superman.imdb_id)
        assert(delete_successful)
        assert(superman not in alice.votes.all())

        # anonymous user case
        superman = Movie.objects.get(title='Superman')
        delete_successful = Movie.delete_vote(None, superman.imdb_id)
        assert(not delete_successful)


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

        assert(user_2 in test_event_1.users.all())

        deactivate_event(test_event_1, user_1)
        test_event_1.users.add(user_3)

        assert(user_3 not in test_event_1.users.all())

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

        assert(user_1 in test_event_1.users.all())

        test_event_1.users.add(user_2)

        assert(user_2 in test_event_1.users.all())

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
        assert(new_lockin in event.lockins.all())

        other_lockin = lockin_event(event.pk, other_user)
        assert(other_lockin not in event.lockins.all())

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
