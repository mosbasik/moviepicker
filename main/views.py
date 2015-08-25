from django.shortcuts import render
from main.models import Movie, WatchEvent, WatchRoom
from django.template import loader, RequestContext

import user_auth


def global_context(request):
    return {
        'user_rooms': request.user.watchroom_set.all(),
    }


def front(request):
    context = {}

    context['rooms'] = WatchRoom.objects.all()
    if request.user.is_authenticated():
        c = RequestContext(request, {'rooms': WatchRoom.objects.all()},
            processors=[global_context])

    return render(request, 'index.html', c)


def all_movies(request):
    context = {}

    return render(request, 'all_movies.html', context)

def add_movie(request):
    context = {}

    return render(request, 'add_movie.html', context)
