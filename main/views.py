from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from main.models import Movie, Event, Group
from django.template import loader, RequestContext
from main.forms import MovieSearchForm, GroupCreationForm, EventCreationForm
from scripts import populate_movies as mov_in

import user_auth


def global_context(request):
    '''
    This is the function to add context variables to all views
    '''
    if request.user.is_authenticated():
        return {
            'user_rooms': request.user.group_set.all(),
            'votes': request.user.votes.all(),
            'search_form': SearchMovieForm(),
        }
    else:
        return {}


def front(request):
    context = {}

    context['rooms'] = Group.objects.all()

    return render(request, 'index.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def all_movies(request):
    context = {}

    context['movies'] = Movie.objects.all().order_by('title')
    context['page_title'] = 'List of all Movies'

    return render(request, 'all_movies.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def add_movie(request):
    context = {}

    if request.method == 'POST':
        url = request.POST.get('url')

        if url:
            # either imdb id or 'failed' or 'not a movie'
            result = mov_in.MovieToPick.make_movie(url)
            if result == 'failed' or result == 'not a movie':
                context['is_movie'] = 'no'
                context['message'] = 'Not a movie'
            else:
                context['is_movie'] = 'yes'
                context['message'] = 'Movie entered'
                context['movie'] = Movie.objects.get(imdb_id=result)

        else:
            context['url_response'] = 'No url was entered'

    return render(request, 'add_movie.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def all_rooms(request):
    context = {}

    context['rooms'] = WatchRoom.objects.all()
    context['page_title'] = 'List of all Rooms'

    return render(request, 'all_rooms.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def user_movies(request):
    context = {}

    # makes the first letter uppercase
    username = request.user.username.title()

    context['movies'] = Movie.objects.filter(voters=request.user).order_by('title')
    context['page_title'] = username + '\'s Liked Movies'

    return render(request, 'all_movies.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def create_vote(request):
    user = request.user
    movie = Movie.objects.get(imdb_id=str(request.POST['id']))

    user.votes.add(movie)
    user.save()

    return HttpResponse(status=200)


def delete_vote(request):
    user = request.user
    movie = Movie.objects.get(imdb_id=request.POST['id'])

    user.votes.remove(movie)
    user.save()

    return HttpResponse(status=200)


def get_votes(request):
    context = {}

    if request.user.is_authenticated():
        votes = request.user.votes.all()
        context['votes'] = votes

    movies = User.votes.all().order_by('title')

    if len(movies) > 0:
        context['movies'] = movies
        return render(request, 'template tk.html', context)


# def user_votes(request, username=None):
#     viewing_user = User.objects.get(username=username)

#     return render(request, 'votes.html', {'viewing_user': viewing_user})

def movie_search(request):
    context = {}
    request_context = RequestContext(request, processors=[global_context])

    if request.method == 'POST':
        form = SearchMovieForm(request.POST)
        context['form'] = form

        if form.is_valid():
            title = form.cleaned_data['title']

            context['movies'] = Movie.objects.filter(title__icontains=title).order_by('title')

            context['message'] = "Here's Your Movies"

            return render_to_response('movie_search.html', context, context_instance=request_context)

        else:
            context['message'] = 'Cannot search for Nothing'
            return render_to_response('movie_search.html', context, context_instance=request_context)

    else:
        form = SearchMovieForm()
        context['form'] = form

        return render_to_response('movie_search.html', context, context_instance=request_context)


def create_room(request):

    context = {}
    request_context = RequestContext(request, processors=[global_context])

    if request.method == 'POST' and request.user.is_authenticated():
        form = GroupCreationForm(request.POST)
        context['form'] = form

        if form.is_valid():
            group_exists = WatchRoom.objects.filter(name__iexact=form.cleaned_data['name']).exists()

            if not group_exists:
                group = WatchRoom()
                group.name = form.cleaned_data['name']
                group.description = form.cleaned_data['description']
                group.created_by = request.user

                group.save()
                context['group'] = group

                context['message'] = "Group created successfully."
                return render_to_response('add_room.html', context, context_instance=request_context)

            else: # group exists
                context['message'] = 'Room name already exists'
                return render_to_response('add_room.html', context, context_instance=request_context)

        else:
            context['message'] = "Room name cannot be blank"
            return render_to_response('add_room.html', context, context_instance=request_context)

    else:
        form = GroupCreationForm()
        context['form'] = form

        return render_to_response('add_room.html', context, context_instance=request_context)


def create_event(request):

    context = {}
    request_context = RequestContext(request, processors=[global_context])

    if request.method == 'POST' and request.user.is_authenticated():
        form = EventCreationForm(request.POST)
        context['form'] = form

        if form.is_valid():
            event = WatchEvent()
            event.event_name = form.cleaned_data['event_name']
            event.date_and_time = form.cleaned_data['date_and_time']
            event.description = form.cleaned_data['description']
            event.created_by = request.user

            event.save()
            context['event'] = event

            context['message'] = "Event created successfully."
            return render_to_response('add_event.html', context, context_instance=request_context)

        else:
            context['message'] = "Sorry, you must be a registered user to create an event."
            return render_to_response('add_event.html', context, context_instance=request_context)

    else:
        form = EventCreationForm()
        context['form'] = form

        return render_to_response('add_event.html', context, context_instance=request_context)
