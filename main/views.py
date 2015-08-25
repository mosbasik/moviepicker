from django.shortcuts import render
from main.models import Movie, WatchEvent, WatchRoom
from django.template import loader, RequestContext

import user_auth


def global_context(request):
    '''
    This is the function to add context variables to all views
    '''
    if request.user.is_authenticated():
        return {
            'user_rooms': request.user.watchroom_set.all(),
        }
    else:
        return {}


def front(request):
    context = {}

    context['rooms'] = WatchRoom.objects.all()

    return render(request, 'index.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def all_movies(request):
    context = {}

    return render(request, 'all_movies.html', context,
        context_instance=RequestContext(request, processors=[global_context]))

def add_movie(request):
    context = {}

    return render(request, 'add_movie.html', context,
        context_instance=RequestContext(request, processors=[global_context]))
