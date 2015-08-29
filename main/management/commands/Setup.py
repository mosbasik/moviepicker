from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from main.models import Movie, WatchEvent, WatchRoom

from scripts import populate_movies as mov_in
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        username = raw_input('Enter name of your SuperUser: ')
        user = User.objects.get(username=username)
        room_exists = WatchRoom.objects.filter(name='World').exists()

        if room_exists:
            print "World Room Exists"
        else:
            print 'Creating Global Room'
            room, created = WatchRoom.objects.get_or_create(created_by=user)
            room.name = 'World'
            room.description = 'Welcome to the World'
            room.save()
            print 'Success!'

        users = User.objects.all()
        print 'Adding Users'
        for user in users:
            world = WatchRoom.objects.get(name='World')
            world.users.add(user)
        print 'Done'

        self._import_movies()


    def _import_movies(self):
        with open('main/static/movie_data.json', 'r') as f:
            data = json.load(f)

        for movie in data['movie']:
            print 'Importing: ' + movie['title']

            result = mov_in.MovieToPick.make_movie(movie['url'])

            if result == 'failed' or result == 'not a movie':
                print 'FAILED'
            else:
                print 'Success!'

        print 'TROLOLOLOLOLOLOLOLOL!!!!11!!111!1'
