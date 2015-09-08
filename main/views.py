# django imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext, loader
from django.utils.text import slugify
from django.views.generic import View
from django.db.models import Count

# local imports
from main.forms import MovieSearchForm, GroupForm, EventForm, LocationForm
from main.functions import get_voted_movie_qs
from main.models import Movie, Event, Group, Location
import user_auth
# from scripts import populate_movies as mov_in

import re


def global_context(request):
    '''
    This is the function to add context variables to all views
    '''
    if request.user.is_authenticated():
        return {
            'user_groups': request.user.movie_groups.exclude(name='World'),
            'user_events': request.user.events.all(),
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


def movies(request):
    context = {}

    search = request.GET.get('search', None)
    order = request.GET.get('order', 'truncated_title')

    if search is not None:
        context['movies'] = Movie.objects.filter(title__icontains=search).order_by(order)
        context['page_title'] = 'Movies containing "%s"' % search

    else:
        context['movies'] = Movie.objects.all().order_by('truncated_title')
        context['page_title'] = 'All Movies'

    return render(
        request, 'movies.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def add_movie(request):
    context = {}

    if request.method == 'POST':

        # extract the IMDB id from the posted URL
        imdb_id = None
        r = r't{2}\d+'
        match = re.search(r, request.POST.get('url', None))
        if match:
            imdb_id = match.group()

        # attempt to submit the movie to the database
        submitted_movie = Movie.submit_movie(request.user.pk, imdb_id)

        # check to see if a movie was successfully submitted
        if submitted_movie is not None:
            context['message'] = 'Movie submitted.'
            context['movie'] = submitted_movie
        else:
            context['message'] = 'Not a movie.'

        return redirect('movie_details', submitted_movie.imdb_id)
    return HttpResponse(status=400)


def all_groups(request):
    context = {}
    context['page_title'] = 'List of all groups'
    context['groups'] = Group.objects.exclude(name='World')
    return render(
        request, 'all_groups.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def user_movies(request):
    user_qs = User.objects.filter(pk=request.user.pk)
    context = {}
    context['page_title'] = request.user.username.title() + "'s Movies"
    context['movies'] = get_voted_movie_qs(user_qs, ['truncated_title'])
    return render(
        request, 'movies.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def create_vote(request):
    user_id = request.user.pk
    imdb_id = request.POST.get('id', None)
    status_code = 200 if Movie.create_vote(user_id, imdb_id) else 400
    return HttpResponse(status=status_code)


def delete_vote(request):
    user_id = request.user.pk
    imdb_id = request.POST.get('id', None)
    status_code = 200 if Movie.delete_vote(user_id, imdb_id) else 400
    return HttpResponse(status=status_code)


def movie_details(request, imdb_id):
    context = {}
    request_context = RequestContext(request, processors=[global_context])

    context['movie'] = Movie.objects.get(imdb_id=imdb_id)
    return render_to_response(
            'movie_details.html', context, context_instance=request_context)


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
                location, created = Location.objects.get_or_create(
                    text=location_form.cleaned_data['text'],
                    group=form.cleaned_data['group'])

                event = Event()
                event.name = form.cleaned_data['name']
                event.date_and_time = form.cleaned_data['date_and_time']
                event.description = form.cleaned_data['description']
                event.group = form.cleaned_data['group']
                event.creator = request.user
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
        event_members = event.users.all()

        context['event'] = event
        context['users'] = event_members
        context['movies'] = get_voted_movie_qs(event_members)
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


def join_event(request, group_slug, event_id):
    if request.user.is_authenticated():
        if Event.objects.filter(id=event_id).exists():
            event = Event.objects.get(id=event_id)
            event.join(request.user.pk)
            return HttpResponse(status=200)
    return HttpResponse(status=401)


def leave_event(request, group_slug, event_id):
    if request.user.is_authenticated():
        if Event.objects.filter(id=event_id).exists():
            event = Event.objects.get(id=event_id)
            event.leave(request.user.pk)
            return HttpResponse(status=200)
    return HttpResponse(status=401)
