#!/usr/bin/env python
import sys, os
import requests
import json
from StringIO import StringIO
import unicodedata

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from main.models import Movie
# from django.conf import settings

# from django.core.files import File
# from django.core.files.temp import NamedTemporaryFile

pattern = '(t{2}[0-9]+)'

movie_id = 'tt0092991'

omdb_api_url = requests.get('http://www.omdbapi.com/?i=%s&plot=full&r=json'
                            % movie_id)

response_dict = omdb_api_url.json()

# import pprint
# pprint.pprint(response_dict)
# print response_dict['Plot']


movie, created = Movie.objects.get_or_create(imdb_id=response_dict['imdbID'])

movie.title = response_dict['Title']
movie.year = response_dict['Year']
movie.imdb_rating = response_dict['imdbRating']
movie.runtime = response_dict['Runtime']
movie.genre = response_dict['Genre']
movie.description = response_dict['Plot']
movie.starring = response_dict['Actors']
movie.written_by = response_dict['Writer']
movie.directed_by = response_dict['Director']

movie.save()
print movie
