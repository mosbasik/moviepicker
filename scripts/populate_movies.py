#!/usr/bin/env python
import sys, os
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
import json
import StringIO
import urllib
import urllib2
from lxml import etree
import re

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from main.models import Movie


class MovieToPick():
    """ Takes a user-input url for an IMDB title and extracts the unique id for
    use with an API and a scraper. Parses the API's json response, along the
    way making sure it's for a movie and only a movie, and adds the poster
    from the scraper to create a movie object and store it in the database --
    if it's not already there. """

    # calls the methods, creates the Movie object, populates the database
    @staticmethod
    def make_movie(url, user=None):
        movie_id_final = MovieToPick._movie_id_from_url(url)
        response_dict = MovieToPick._get_movie_json(movie_id_final)
        # if the user happened to input a TV show and triggers json response,
        # makes sure we don't store with the poster even as a local tempfile
        if response_dict is not None:
            movie = MovieToPick._movie_info(response_dict, movie_id_final, user=None)
            return movie_id_final
        else:
            return 'not a movie'

    # runs regex on user input to extract the unique IMDB movie id
    @staticmethod
    def _movie_id_from_url(url):
        movie_id_pattern = '(t{2}[0-9]+)'
        movie_id_match = re.search(movie_id_pattern, '%s' % url)
        if movie_id_match is not None:
            movie_id_final = movie_id_match.group()
        else:
            movie_id_final = None

        # returns an id or None
        return movie_id_final

    # uses the movie id to hit the omdb API;
    # excludes TV shows, person pages, etc.
    @staticmethod
    def _get_movie_json(movie_id_final):
        if movie_id_final is not None:
            omdb_api_url = requests.get('http://www.omdbapi.com/?i=%s&plot=full&r=json'
                            % movie_id_final)

            response_dict = omdb_api_url.json()

            if response_dict['Type'] == 'movie':
                return response_dict
        else:
            return None

    # import pprint
    # pprint.pprint(response_dict)
    # print response_dict['Plot']

    # the API doesn't include the movie poster, so we get that one
    # ourselves with a quick scrape.
    @staticmethod
    def _get_poster(movie_id_final):
        result = urllib.urlopen("http://www.imdb.com/title/%s/" % movie_id_final)
        html = result.read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(html), parser)

        # import ipdb; ipdb.set_trace()

        poster_xpath = '//*[@id="img_primary"]/div[1]/a/img/@src'
        poster = tree.xpath(poster_xpath)

        # there's only ever one poster -- unless there isn't one.
        if len(poster) == 1:
            poster = poster[0]
            poster_response = urllib.urlopen(poster).read()
            poster_temp = NamedTemporaryFile(delete=True)
            poster_temp.write(poster_response)
            # import ipdb; ipdb.set_trace()
            return poster_temp
        else:
            return None

    # pulls in the poster tempfile for unpacking and inclusion
    # in the creation of the movie object
    @staticmethod
    def _movie_info(response_dict, movie_id_final, user=None):
        movie_image = MovieToPick._get_poster(movie_id_final)
        # import ipdb; ipdb.set_trace()

        # in case the json parser returned None
        if response_dict:

            movie_exists = Movie.objects.filter(imdb_id=response_dict['imdbID']).exists()

            if not movie_exists:
                movie = Movie()
                movie.imdb_id = response_dict['imdbID']
                movie.title = response_dict['Title']
                movie.year = response_dict['Year']

                # movies not yet released do not have ratings
                try:
                    movie.imdb_rating = float(response_dict['imdbRating'])
                except ValueError:
                    pass

                movie.runtime = response_dict['Runtime']
                movie.genre = response_dict['Genre']
                movie.description = response_dict['Plot']
                movie.starring = response_dict['Actors']
                movie.written_by = response_dict['Writer']
                movie.directed_by = response_dict['Director']

                if movie_image is not None:
                    movie.poster.save('%s.jpg' % movie.title, File(movie_image))

                # this doesn't work yet to assign a creator to each movie:
                if user is not None:
                    movie.created_by = user

                movie.save()
                return movie
            else:
                return Movie.objects.get(imdb_id=movie_id_final)

        else:
            return 'failed'
