#!/usr/bin/env python
import sys, os
import requests
import json
from StringIO import StringIO

# sys.path.append('..')
# os.environ.setdefault("DJANGO_SETTING_MODULE", "project.settings")

# from main.models import Movie
# from django.conf import settings

# from django.core.files import File
# from django.core.files.temp import NamedTemporaryFile

pattern = '(t{2}[0-9]+)'

movie_id = 'tt0092991'

omdb_api_url = requests.get('http://www.omdbapi.com/?i=%s&plot=full&r=json'
                            % movie_id)

response_dict = omdb_api_url.json()
# print response_dict
# print response_dict['Plot']

for data in response_dict:
    movie, created = Movie.objects.get_or_create(imdb_id=data.get('imdbID'))

    movie.title = data.get('Title')
    movie.year = data.get('Year')
    movie.imdb_rating = data.get('imdbRating')
    movie.runtime = data.get('Runtime')
    movie.genre = data.get('Genre')
    movie.description = data.get('Plot')
    movie.starring = data.get('Actors')
    movie.written_by = data.get('Writer')
    movie.directed_by = data.get('Director')

    movie.save()
    print movie





