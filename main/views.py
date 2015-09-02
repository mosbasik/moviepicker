# django imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.utils.text import slugify
from django.views.generic import View

# local imports
from main.forms import MovieSearchForm, GroupForm, EventForm, LocationForm
from main.functions import get_voted_movie_qs
from main.models import Movie, Event, Group, Location
from scripts import populate_movies as mov_in

import user_auth


def global_context(request):
    '''
    This is the function to add context variables to all views
    '''
    if request.user.is_authenticated():
        return {
            'user_groups': request.user.movie_groups.all(),
            'votes': request.user.votes.all(),
            'search_form': MovieSearchForm(),
        }
    else:
        return {}


def front(request):
    context = {}

    context['rooms'] = Group.objects.all()

    return render(
        request, 'index.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def all_movies(request):
    context = {}
    context['movies'] = get_voted_movie_qs(User.objects.all(), include_unvoted=True)
    context['page_title'] = 'List of all Movies'
    return render(
        request, 'all_movies.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def add_movie(request):
    context = {}
    user = request.user

    if request.method == 'POST':
        url = request.POST.get('url')

        if url:
            # either imdb id or 'failed' or 'not a movie'
            result = mov_in.MovieToPick.make_movie(url, user)
            print result
            if result == 'failed' or result == 'not a movie':
                context['is_movie'] = 'no'
                context['message'] = 'Not a movie'
            else:
                context['is_movie'] = 'yes'
                context['message'] = 'Movie entered'
                context['movie'] = Movie.objects.get(imdb_id=result)

        else:
            context['url_response'] = 'No url was entered'

    return render(
        request, 'add_movie.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def all_groups(request):
    context = {}
    context['page_title'] = 'List of all groups'
    context['groups'] = Group.objects.all()
    return render(
        request, 'all_groups.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def user_movies(request):
    user_qs = User.objects.filter(pk=request.user.pk)
    context = {}
    context['page_title'] = request.user.username.title() + "'s Movies"
    context['movies'] = get_voted_movie_qs(user_qs, ['truncated_title'])
    return render(
        request, 'all_movies.html', context,
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


# DON'T DELETE THIS RIGHT AWAY, I'M NOT SURE IF IT'S USED BY ANYTHING

# def get_votes(request):
#     context = {}

#     if request.user.is_authenticated():
#         votes = request.user.votes.all()
#         context['votes'] = votes

#     movies = User.votes.all().order_by('truncated_title')

#     if len(movies) > 0:
#         context['movies'] = movies
#         return render(request, 'template tk.html', context)


def movie_search(request):
    context = {}
    request_context = RequestContext(request, processors=[global_context])

    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        context['form'] = form

        if form.is_valid():
            title = form.cleaned_data['title']

            context['movies'] = Movie.objects.filter(
                title__icontains=title).order_by('truncated_title')

            context['message'] = "Here's Your Movies"

            return render_to_response(
                'movie_search.html', context, context_instance=request_context)

        else:
            context['message'] = 'Cannot search for Nothing'
            return render_to_response(
                'movie_search.html', context, context_instance=request_context)

    else:
        form = MovieSearchForm()
        context['form'] = form

        return render_to_response(
            'movie_search.html', context, context_instance=request_context)


def create_group(request):

    context = {}
    request_context = RequestContext(request, processors=[global_context])

    if request.method == 'POST' and request.user.is_authenticated():
        form = GroupForm(request.POST)
        context['form'] = form

        if form.is_valid():
            group_exists = Group.objects.filter(
                name__iexact=form.cleaned_data['name']).exists()

            if not group_exists:
                group = Group()
                group.name = form.cleaned_data['name']
                group.description = form.cleaned_data['description']
                group.creator = request.user

                group.save()
                context['group'] = group

                context['message'] = "Group created successfully."
                return render_to_response(
                    'add_group.html', context,
                    context_instance=request_context)

            else:   # group exists
                context['message'] = 'Group name already exists'
                return render_to_response(
                    'add_group.html', context,
                    context_instance=request_context)

        else:
            context['message'] = "Group name cannot be blank"
            return render_to_response(
                'add_group.html', context, context_instance=request_context)

    else:
        form = GroupForm()
        context['form'] = form

        return render_to_response(
            'add_group.html', context, context_instance=request_context)


class CreateEvent(View):

    def post(self, request):
        context = {}
        request_context = RequestContext(request, processors=[global_context])

        if request.method == 'POST' and request.user.is_authenticated():
            form = EventForm(request.POST)
            location_form = LocationForm(request.POST)
            context['form'] = form
            context['location'] = location_form

            if form.is_valid() and location_form.is_valid():
                # old = []
                # old = Location.objects.filter(Q(url__iexact=location_form.cleaned_data['url']) | Q(text__iexact=location_form.cleaned_data['text']))
                location, created = Location.objects.get_or_create(
                    text=location_form.cleaned_data['text'],
                    group=form.cleaned_data['group'])
                # location.text = location_form.cleaned_data['text']
                # location.group = form.cleaned_data['group'].id

                event = Event()
                event.name = form.cleaned_data['name']
                event.date_and_time = form.cleaned_data['date_and_time']
                event.description = form.cleaned_data['description']
                event.group = form.cleaned_data['group']
                event.created_by = request.user
                event.location = location

                event.save()

                context['event'] = event

                context['message'] = "Event created successfully."
                return render_to_response(
                    'add_event.html', context,
                    context_instance=request_context)
            else:
                context['message'] = form.errors
                context['errors'] = location_form.errors
                return render_to_response(
                    'add_event.html', context,
                    context_instance=request_context)

        else:
            context['message'] = "Sorry, you must be a registered user."
            return render_to_response(
                'add_event.html', context,
                context_instance=request_context)

    def get(self, request):
        context = {}
        user = request.user
        request_context = RequestContext(request, processors=[global_context])
        form = EventForm()
        location_form = LocationForm()
        context['form'] = form
        context['location'] = location_form

        return render_to_response(
            'add_event.html', context, context_instance=request_context)


def group_details(request, group_slug):

    context = {}
    request_context = RequestContext(request, processors=[global_context])

    group = Group.objects.get(slug=group_slug)
    group_members = group.users.all()

    group_movies = Movie.objects.filter(voters__in=group_members)
    group_movies = group_movies.annotate(num_votes=Count('voters'))
    group_movies = group_movies.order_by('-num_votes').distinct()

    context['group'] = group
    context['users'] = group_members
    context['movies'] = get_voted_movie_qs(group_members)

    return render_to_response(
            'group_details.html', context, context_instance=request_context)


def all_events(request):
    context = {}
    request_context = RequestContext(request, processors=[global_context])
    context['events'] = Event.objects.all()

    return render_to_response(
        'all_events.html', context, context_instance=request_context)


class EventDetails(View):

    def get(self, request, group_slug, event_id):
        context = {}
        request_context = RequestContext(request, processors=[global_context])
        event = Event.objects.get(id=event_id)
        users = event.users.all()
        movies = Movie.objects.filter(voters__in=users)

        context['event'] = event
        context['users'] = users
        context['movies'] = movies
        return render_to_response(
            'event_details.html', context, context_instance=request_context)


def join_group(request, group_slug):
    if request.user.is_authenticated():
        group = Group.objects.get(slug=request.POST.get('group_slug', None))
        group.users.add(request.user)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


def leave_group(request, group_slug):
    if request.user.is_authenticated():
        group = Group.objects.get(slug=request.POST.get('group_slug', None))
        group.users.remove(request.user)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)
