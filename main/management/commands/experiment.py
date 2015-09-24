from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import Movie, Event, Group, Location, LockIn, Viewing

from scripts import populate_movies as mov_in
import json


class Command(BaseCommand):

    def handle(self, *args, **options):

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
