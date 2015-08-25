from django.shortcuts import render
from main.models import Movie, WatchEvent, WatchRoom

import user_auth


def front(request):
    context = {}

    context['rooms'] = WatchRoom.objects.all()
    if request.user.is_authenticated():
        context['user_rooms'] = request.user.watchroom_set.all()

    return render(request, 'index.html', context)


def all_movies(request):
    context = {}

    return render(request, 'all_movies.html', context)

def add_movie(request):
    context = {}

    return render(request, 'add_movie.html', context)
