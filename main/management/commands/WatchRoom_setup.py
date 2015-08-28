from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from main.models import Movie, WatchEvent, WatchRoom

from scripts import populate_movies as mov_in
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print 'Creating Global Room'
        room, created = WatchRoom.objects.get_or_create(name='Universal')
        room.description = 'Welcome to the World'

        room.save()
        print 'Success!'

        with open('main/static/movie_data.json', 'r') as f:
            data = json.load(f)
            self._import_movies(data)



    def _import_movies(self, data):
        for movie in data['movie']:
            print 'Importing: ' + movie['title']

            result = mov_in.MovieToPick.make_movie(movie['url'])

            if result == 'failed' or result == 'not a movie':
                print 'FAILED'
            else:
                print 'Success!'

        print 'TROLOLOLOLOLOLOLOLOL!!!!11!!111!1'
