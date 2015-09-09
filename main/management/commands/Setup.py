from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from main.models import Movie, Event, Group, Location

from scripts import populate_movies as mov_in
import json
import re


class Command(BaseCommand):

    def handle(self, *args, **options):
        username = raw_input('Enter name of your SuperUser: ')
        user = User.objects.get(username=username)
        super_user = user
        room_exists = Group.objects.filter(name='World').exists()

        if room_exists:
            print "World Group Exists"
        else:
            print 'Creating Global Group'
            room, created = Group.objects.get_or_create(creator=user)
            room.name = 'World'
            room.description = 'Every user is added to the "World" group automatically upon registration.'
            room.save()
            print 'Success!'

        users = User.objects.all()
        print 'Adding Users'
        for user in users:
            world = Group.objects.get(name='World')
            world.users.add(user)
        print 'Done'

        self._import_movies(super_user)
        self._populate_testing_data(super_user)

    def _import_movies(self, user):
        with open('main/static/setup_scripts/movie_data.json', 'r') as f:
            data = json.load(f)

        for movie in data['movie']:
            print 'Importing: ' + movie['title']

            # extract the IMDB id from the URL
            imdb_id = None
            r = r't{2}\d+'
            match = re.search(r, movie['url'])
            if match:
                imdb_id = match.group()

            result = Movie.submit_movie(user.pk, imdb_id)

            print 'Success!' if result is not None else 'FAILED.'

        print 'Finished'

    def _populate_testing_data(self, super_user):
        print "It's started"
        with open('main/static/setup_scripts/groups.json', 'r') as f:
            data = json.load(f)

        user_list = []
        group_list = []
        event_list = []
        movie_list = Movie.objects.all()

        for user in data['users']:
            print 'Creating: ' + user['username']
            new_user, created = User.objects.get_or_create(
                username=user['username'], email=user['email'],
            )
            if created:
                new_user.set_password(user['password'])
            user_list.append(new_user)

        print 'Users created.'

        for i, group in enumerate(data['groups']):
            print 'Creating: ' + group['name']

            new_group, created = Group.objects.get_or_create(
                name=group['name'],
                description=group['description'],
                creator=super_user,
            )
            new_group.users.add(user_list[i])
            new_group.users.add(user_list[i+1])
            new_group.users.add(user_list[i+3])
            new_group.users.add(user_list[i+5])

            group_list.append(new_group)

        print "Groups created."

        for i, event in enumerate(data['events']):
            print 'Creating: ' + event['name']

            new_location, created = Location.objects.get_or_create(
                text=event['location'], group=group_list[i])

            new_event, created = Event.objects.get_or_create(
                name=event['name'], date_and_time=event['date_and_time'],
                description=event['description'], group=group_list[i],
                creator=super_user, location=new_location)
            new_event.users.add(user_list[i])
            new_event.users.add(user_list[i+2])
            new_event.users.add(user_list[i+3])

            event_list.append(new_event)

        print 'Events created.'

        for i, user in enumerate(user_list):
            user.votes.clear()
            user.votes.add(movie_list[i])
            user.votes.add(movie_list[i+1])
            user.votes.add(movie_list[i+3])
            user.votes.add(movie_list[i+5])
            user.votes.add(movie_list[i+8])
            user.votes.add(movie_list[i+12])
            user.votes.add(movie_list[i+15])
            user.votes.add(movie_list[i+20])

        print "Movie votes have been added"

        print "All done!"
