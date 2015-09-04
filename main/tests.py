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


@skip
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
            imdb_id='tt1408101',
            title='Star Trek Into Darkness')
        trek = Movie.objects.create(
            imdb_id='tt0796366',
            title='Star Trek')
        star_wars = Movie.objects.create(
            imdb_id='tt0076759',
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

    def test_group_creation(self):
        '''Authed users can create groups; anonymous users can't.'''

        # registered user case
        alice = User.objects.get(username='alice')

        # group name already exists
        alpha, msg = Group.create_group(alice.pk, 'Alpha')
        assert(msg == 'Group name already exists.')
        assert(alpha is None)

        # with description
        bravo, msg = Group.create_group(alice.pk, 'Bravo', description='second')
        assert(msg == 'Group "Bravo" created successfully.')
        assert(Group.objects.filter(pk=bravo.pk).exists())
        assert(bravo.creator == alice)
        assert(bravo.name == 'Bravo')
        assert(bravo.description == 'second')

        # without description
        charlie, msg = Group.create_group(alice.pk, 'Charlie')
        assert(msg == 'Group "Charlie" created successfully.')
        assert(Group.objects.filter(pk=charlie.pk).exists())
        assert(charlie.creator == alice)
        assert(charlie.name == 'Charlie')
        assert(charlie.description is None)

        # anonymous user case
        delta, msg = Group.create_group(None, 'Delta')
        assert(msg == 'Only registered users can create groups.')
        assert(delta is None)

    def test_group_join(self):
        '''Authed users can join groups; anonymous users can't.'''

        # registered user case
        eve = User.objects.get(username='eve')
        alpha = Group.objects.get(name='Alpha')
        assert(eve not in alpha.users.all())
        join_succeeded = alpha.join(eve.pk)
        assert(join_succeeded)
        assert(eve in alpha.users.all())

        # anonymous user case
        alpha = Group.objects.get(name='Alpha')
        join_succeeded = alpha.join(None)
        assert(not join_succeeded)

    def test_group_leave(self):
        '''Authed users can leave groups; anonymous users can't.'''

        # registered user case
        alice = User.objects.get(username='alice')
        alpha = Group.objects.get(name='Alpha')
        assert(alice in alpha.users.all())
        leave_succeeded = alpha.leave(alice.pk)
        assert(leave_succeeded)
        assert(alice not in alpha.users.all())

        # anonymous user case
        alpha = Group.objects.get(name='Alpha')
        leave_succeeded = alpha.leave(None)
        assert(not leave_succeeded)

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


# @skip
class EventTestCase(TestCase):

    def setUp(self):

        # movie setup
        trek_into_darkness = Movie.objects.create(
            imdb_id='tt1408101',
            title='Star Trek Into Darkness')
        trek = Movie.objects.create(
            imdb_id='tt0796366',
            title='Star Trek')
        star_wars = Movie.objects.create(
            imdb_id='tt0076759',
            title='Star Wars: Episode IV - A New Hope')
        titanic = Movie.objects.create(
            imdb_id='tt0120338',
            title='Titanic')
        avatar = Movie.objects.create(
            imdb_id='tt0499549',
            title='Avatar')
        raiders = Movie.objects.create(
            imdb_id='tt0082971',
            title='Raiders of the Lost Ark')

        # user setup
        alice = User.objects.create(username='alice')
        bob = User.objects.create(username='bob')
        eve = User.objects.create(username='eve')

        # vote setup
        alice.votes.add(trek_into_darkness)
        bob.votes.add(trek)
        eve.votes.add(star_wars)
        eve.votes.add(trek)

        # group setup
        alpha = Group.objects.create(name='Alpha', creator=alice)
        alpha.users.add(alice)
        alpha.users.add(bob)

        # event setup
        e1 = Event.objects.create(name='E1', group=alpha, creator=alice)
        e1.users.add(alice)
        e1.users.add(bob)
        LockIn.objects.create(event=e1, movie=raiders)
        LockIn.objects.create(event=e1, movie=titanic)
        LockIn.objects.create(event=e1, movie=avatar)

        e2 = Event.objects.create(name='E2', group=alpha, creator=alice)
        e2.users.add(alice)

        e3 = Event.objects.create(name='E3', group=alpha, creator=alice)
        e3.users.add(alice)

        e4 = Event.objects.create(name='E4', group=alpha, creator=alice, is_active=False)
        e4.users.add(alice)

        e5 = Event.objects.create(name='E5', group=alpha, creator=alice, is_active=False)
        e5.users.add(alice)

        # location setup
        basement = Location.objects.create(text='basement', group=alpha)

        # viewing setup
        Viewing.objects.create(event=e1, movie=raiders, user=alice)
        Viewing.objects.create(event=e1, movie=raiders, user=eve)
        Viewing.objects.create(event=e1, movie=raiders, user=bob)

    def test_event_create(self):
        '''Only authed group members can create events.'''

        # member basic event
        alice = User.objects.get(username='alice')
        alpha = Group.objects.get(name='Alpha')
        alice_event_count = alice.events_created.all().count()
        alt_rock = alpha.create_event(alice.pk, 'Alt Rock')
        assert(alice.events_created.all().count() == alice_event_count + 1)
        assert(alt_rock is not None)
        assert(alt_rock.name == 'Alt Rock')
        assert(alt_rock.group == alpha)
        assert(alt_rock.creator == alice)

        # member fancy event
        bob = User.objects.get(username='bob')
        alpha = Group.objects.get(name='Alpha')
        basement = Location.objects.filter(group=alpha).get(text='basement')
        bob_event_count = bob.events_created.all().count()
        bass_music = alpha.create_event(
            bob.pk,
            'Bass Music',
            date_and_time='2015-10-19 21:30',
            description='feat. Techmaster P.E.B.',
            location=basement
        )
        assert(bob.events_created.all().count() == bob_event_count + 1)
        assert(bass_music is not None)
        assert(bass_music.name == 'Bass Music')
        assert(bass_music.group == alpha)
        assert(bass_music.creator == bob)
        assert(bass_music.date_and_time == '2015-10-19 21:30')
        assert(bass_music.description == 'feat. Techmaster P.E.B.')
        assert(bass_music.location == basement)

        # non-member case
        eve = User.objects.get(username='eve')
        alpha = Group.objects.get(name='Alpha')
        eve_event_count = eve.events_created.all().count()
        zamrock = alpha.create_event(eve.pk, 'Zamrock')
        assert(eve.events_created.all().count() == eve_event_count)
        assert(zamrock is False)

        # anonymous user case
        alpha = Group.objects.get(name='Alpha')
        yodeling = alpha.create_event(None, 'Yodeling')
        assert(yodeling is False)

    def test_event_deactivate(self):
        '''Only the event creator can set an active event to inactive.'''

        # creator case
        alice = User.objects.get(username='alice')
        e2 = Event.objects.get(name='E2')
        assert(e2.is_active)
        e2.deactivate(alice.pk)
        assert(not e2.is_active)

        # non-creator case
        eve = User.objects.get(username='eve')
        e3 = Event.objects.get(name='E3')
        assert(e3.is_active)
        e3.deactivate(eve.pk)
        assert(e3.is_active)

        # anonymous case
        e3 = Event.objects.get(name='E3')
        assert(e3.is_active)
        e3.deactivate(None)
        assert(e3.is_active)

    def test_event_activate(self):
        '''Only the event creator can set an inactive event to active.'''

        # creator case
        alice = User.objects.get(username='alice')
        e4 = Event.objects.get(name='E4')
        assert(not e4.is_active)
        e4.activate(alice.pk)
        assert(e4.is_active)

        # non-creator case
        eve = User.objects.get(username='eve')
        e5 = Event.objects.get(name='E5')
        assert(not e5.is_active)
        e5.activate(eve.pk)
        assert(not e5.is_active)

        # anonymous case
        e5 = Event.objects.get(name='E5')
        assert(not e5.is_active)
        e5.activate(None)
        assert(not e5.is_active)

    def test_event_join_active(self):
        '''Any site user can join an active event.'''

        # group member case
        bob = User.objects.get(username='bob')
        e2 = Event.objects.get(name='E2')
        assert(bob not in e2.users.all())
        e2.join(bob.pk)
        assert(bob in e2.users.all())

        # site user but not group member case
        eve = User.objects.get(username='eve')
        e2 = Event.objects.get(name='E2')
        assert(eve not in e2.users.all())
        e2.join(eve.pk)
        assert(eve in e2.users.all())

        # anonymous user case
        e2 = Event.objects.get(name='E2')
        e2_initial_member_count = e2.users.all().count()
        e2.join(None)
        assert(e2.users.all().count() == e2_initial_member_count)

    def test_event_join_inactive(self):
        '''No one can join join an inactive event.'''

        # group member case
        bob = User.objects.get(username='bob')
        e4 = Event.objects.get(name='E4')
        assert(bob not in e4.users.all())
        e4.join(bob.pk)
        assert(bob not in e4.users.all())

        # site user but not group member case
        eve = User.objects.get(username='eve')
        e4 = Event.objects.get(name='E4')
        assert(eve not in e4.users.all())
        e4.join(eve.pk)
        assert(eve not in e4.users.all())

        # anonymous user case
        e4 = Event.objects.get(name='E4')
        e4_initial_member_count = e4.users.all().count()
        e4.join(None)
        assert(e4.users.all().count() == e4_initial_member_count)

    def test_event_movies(self):
        '''In an event, only event member movies are included.'''

        e1_movies = Event.objects.get(name='E1').movie_pool()

        assert(e1_movies.all().count() == 2)
        e1_movies = e1_movies.distinct()
        assert(e1_movies.all().count() == 2)

        trek_movies = Movie.objects.filter(title__icontains='trek')
        for movie in e1_movies:
            assert(movie in trek_movies)

    def test_event_vote_count(self):
        '''In an event, only event member movie votes are counted.'''

        e1_movies = Event.objects.get(name='E1').movie_pool()
        trek = e1_movies.get(title='Star Trek')
        assert(trek.num_votes == 1)

    def test_event_lockin(self):
        '''A movie can only be locked in to an event by the event creator.'''

        # creator case
        e1 = Event.objects.get(name='E1')
        alice = User.objects.get(username='alice')
        trek = Movie.objects.get(title='Star Trek')
        assert(trek not in e1.watched_movies.all())
        lockin_successful = e1.lockin(alice.pk, trek.pk)
        assert(lockin_successful)
        assert(trek in e1.watched_movies.all())

        # non creator case
        bob = User.objects.get(username='bob')
        trek_into_darkness = Movie.objects.get(title='Star Trek Into Darkness')
        assert(trek_into_darkness not in e1.watched_movies.all())
        lockin_successful = e1.lockin(bob.pk, trek_into_darkness.pk)
        assert(not lockin_successful)
        assert(trek_into_darkness not in e1.watched_movies.all())

        # anonymous case
        assert(trek_into_darkness not in e1.watched_movies.all())
        lockin_successful = e1.lockin(None, trek_into_darkness)
        assert(trek_into_darkness not in e1.watched_movies.all())

    def test_event_lockin_remove(self):
        '''A locked in movie can only removed from an event by the event creator.'''

        # creator case
        e1 = Event.objects.get(name='E1')
        alice = User.objects.get(username='alice')
        titanic = Movie.objects.get(title='Titanic')
        assert(titanic in e1.watched_movies.all())
        lockin_remove_successful = e1.lockin_remove(alice.pk, titanic.pk)
        assert(lockin_remove_successful)
        assert(titanic not in e1.watched_movies.all())

        # non creator case
        bob = User.objects.get(username='bob')
        avatar = Movie.objects.get(title='Avatar')
        assert(avatar in e1.watched_movies.all())
        lockin_remove_successful = e1.lockin_remove(bob.pk, avatar.pk)
        assert(not lockin_remove_successful)
        assert(avatar not in e1.watched_movies.all())

        # anonymous case
        assert(avatar not in e1.watched_movies.all())
        lockin_remove_successful = e1.lockin_remove(None, avatar)
        assert(avatar not in e1.watched_movies.all())

    def test_event_lockin_create_viewings(self):
        '''Locking in a movie creates a viewing of it for all event members.'''

        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        eve = User.objects.get(username='eve')
        e1 = Event.objects.get(name='E1')
        trek = Movie.objects.get(title='Star Trek')

        assert(not Viewing.objects.filter(event=e1, user=alice, movie=trek).exists())
        assert(not Viewing.objects.filter(event=e1, user=bob, movie=trek).exists())
        assert(not Viewing.objects.filter(event=e1, user=eve, movie=trek).exists())

        e1.lockin(alice.pk, trek.pk)

        assert(Viewing.objects.filter(event=e1, user=alice, movie=trek).exists())
        assert(Viewing.objects.filter(event=e1, user=bob, movie=trek).exists())
        assert(not Viewing.objects.filter(event=e1, user=eve, movie=trek).exists())

    def test_event_lockin_remove_delete_viewings(self):
        '''Removing a locked in movie deletes its viewing from all event members.'''

        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        eve = User.objects.get(username='eve')
        e1 = Event.objects.get(name='E1')
        raiders = Movie.objects.get(title='Raiders of the Lost Ark')

        assert(Viewing.objects.filter(event=e1, user=alice, movie=raiders).exists())
        assert(Viewing.objects.filter(event=e1, user=bob, movie=raiders).exists())
        assert(Viewing.objects.filter(event=e1, user=eve, movie=raiders).exists())

        e1.lockin_remove(alice.pk, raiders.imdb_id)

        assert(not Viewing.objects.filter(event=e1, user=alice, movie=raiders).exists())
        assert(not Viewing.objects.filter(event=e1, user=bob, movie=raiders).exists())
        assert(Viewing.objects.filter(event=e1, user=eve, movie=raiders).exists())

    def test_event_join_creates_viewings(self):
        '''Users joining an event w/existing lock ins get viewings for all.'''

        eve = User.objects.get(username='eve')
        e1 = Event.objects.get(name='E1')
        titanic = Movie.objects.get(title='Titanic')
        avatar = Movie.objects.get(title='Avatar')

        assert(not Viewing.objects.filter(event=e1, user=eve, movie=titanic).exists())
        assert(not Viewing.objects.filter(event=e1, user=eve, movie=avatar).exists())

        e1.join(eve.pk)

        assert(Viewing.objects.filter(event=e1, user=eve, movie=titanic).exists())
        assert(Viewing.objects.filter(event=e1, user=eve, movie=avatar).exists())
