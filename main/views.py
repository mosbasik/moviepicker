# django imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext, loader
from django.utils.text import slugify
from django.views.generic import View
from django.db.models import Count
from django.core.urlresolvers import reverse

# local imports
from main.forms import (
    MovieSearchForm,
    GroupForm,
    EventForm,
    LocationForm,
    LockInForm,
)
from main.functions import get_voted_movie_qs
from main.models import Movie, Event, Group, Location, LockIn
import user_auth

# python imports
import re


# don't know if uses model functions
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


class Home(View):

    def get(self, request):
        if request.user.is_authenticated():
            request_context = RequestContext(request, processors=[global_context])
            u = request.user
            context = {}
            context['movies'] = u.votes.all().order_by('truncated_title')
            context['movies_label'] = 'Movies you\'ve voted for:'
            context['groups_joined'] = u.movie_groups.all().order_by('name')
            context['events_joined'] = u.events.all().order_by('date_and_time')
            context['groups_created'] = u.groups_created.all().order_by('name')
            context['events_created'] = u.events_created.all().order_by('date_and_time')
            return render(request, 'home.html', context, request_context)
        else:
            return redirect('movies')

    def post(self, request):
        pass


# don't know if uses model functions
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
        'movie_details.html',
        context,
        context_instance=request_context
    )


@login_required
def create_group(request):

    context = {}
    context['form'] = GroupForm()
    request_context = RequestContext(request, processors=[global_context])

    # if the view was called with a POST
    if request.method == 'POST':

        # get the filled form object from the request
        form = GroupForm(request.POST)

        # save it into the context so it can be reused if it doesn't validate
        context['form'] = form

        # if the submitted form validates
        if form.is_valid():

            # attempt to create the new group
            group, context['message'] = Group.create_group(
                request.user.pk,
                form.cleaned_data['name'],
                form.cleaned_data['description'],
            )

            # if the group was created, redirect new owner to its details page
            if group is not None:
                return redirect('group_details', group_slug=group.slug)

        # if the submitted form does not pass all validation
        else:
            context['message'] = "Group name cannot be blank."

    return render_to_response(
        'add_group.html',
        context,
        context_instance=request_context
    )


# don't know if uses model functions
class CreateEvent(View):

    def post(self, request):
        context = {}
        request_context = RequestContext(request, processors=[global_context])

        if request.method == 'POST' and request.user.is_authenticated():
            form = EventForm(request.user, request.POST)
            location_form = LocationForm(request.POST)
            context['form'] = form
            context['location'] = location_form

            if form.is_valid() and location_form.is_valid():
                location, created = Location.objects.get_or_create(
                    text=location_form.cleaned_data['text'],
                    group=form.cleaned_data['group'])
                print form.cleaned_data['date_and_time']
                name = form.cleaned_data['name']
                date_and_time = form.cleaned_data['date_and_time']
                description = form.cleaned_data['description']
                group = form.cleaned_data['group']

                event = group.create_event(
                    request.user.pk, name, date_and_time, description,
                    location)

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
        form = EventForm(user=request.user)
        location_form = LocationForm()
        context['form'] = form
        context['location'] = location_form

        return render_to_response(
            'add_event.html', context, context_instance=request_context)


def event_list(request):
    context = {}
    request_context = RequestContext(request, processors=[global_context])
    context['events'] = Event.objects.all()

    return render_to_response(
        'all_events.html',
        context,
        context_instance=request_context
    )


class GroupPost(View):

    def post(self, request, group_slug=None):

        # if user is authenticated
        if request.user.is_authenticated():
            action = request.POST.get('action', None)
            slug = request.POST.get('group_slug', None)
            if Group.objects.filter(slug=slug).exists():
                group = Group.objects.get(slug=slug)
                if action == 'join':
                    group.join(request.user.pk)
                elif action == 'leave':
                    group.leave(request.user.pk)
                else:
                    # bad request; invalid action recieved
                    return HttpResponse(status=400)

                # successful operation
                return HttpResponse(status=200)

            # bad request; invalid group recieved
            return HttpResponse(status=400)

        # if user is not authenticated
        else:
            # redirect to login page (saving referral URL to get back)
            temp_resp = redirect('login')
            redirect_url = temp_resp['location'] + '?next=%s' % request.path
            return JsonResponse({'redirect': redirect_url})


class GroupList(GroupPost):

    def get(self, request):
        request_context = RequestContext(request, processors=[global_context])

        context = {}
        context['page_title'] = 'List of all groups'
        context['groups'] = Group.objects.exclude(name='World')

        return render_to_response(
            'group_list.html',
            context,
            context_instance=request_context
        )


class GroupDetails(GroupPost):

    def get(self, request, group_slug):
        request_context = RequestContext(request, processors=[global_context])

        group = Group.objects.get(slug=group_slug)

        context = {}
        context['group'] = group
        context['users'] = group.users.all()
        context['movies_label'] = 'Movies that group members have voted for:'
        context['movies'] = group.movie_pool().order_by('-num_votes').distinct()

        return render_to_response(
            'group_details.html',
            context,
            context_instance=request_context
        )


class EventDetails(View):

    def get(self, request, group_slug, event_id):
        request_context = RequestContext(request, processors=[global_context])

        event = Event.objects.get(id=event_id)
        event_members = event.users.all()
        lockin_form = LockInForm(event=event)

        context = {}
        context['lockin_form'] = lockin_form
        context['event'] = event
        context['movies_label'] = 'Movies that event attendees have voted for:'
        context['movies'] = event.movie_pool().order_by('-num_votes', '-imdb_rating').distinct()

        return render_to_response(
            'event_details.html',
            context,
            context_instance=request_context
        )

    def post(self, request, group_slug, event_id):
        context = {}
        event = Event.objects.get(id=event_id)
        request_context = RequestContext(request, processors=[global_context])
        if request.POST['type'] == 'lockin':
            lockin_form = LockInForm(event, request.POST)

            if lockin_form.is_valid():
                movie = lockin_form.cleaned_data['movie']
                event.lockin(request.user.pk, movie.imdb_id)
                context['success'] = 'Your movie has been locken in'
                return HttpResponseRedirect(reverse(
                    'event_details', args=[group_slug, event_id]))
            context['errors'] = form.errors
            return render_to_response(
                'event_details.html', context,
                context_instance=request_context)
        elif request.POST['type'] == 'delete':
            movie = request.POST['movie']
            event.lockin_remove(request.user.pk, movie)
            context['success'] = 'Your movie has been locken in'
            return HttpResponseRedirect(reverse(
                    'event_details', args=[group_slug, event_id]))
            context['errors'] = form.errors
            return render_to_response(
                'event_details.html', context,
                context_instance=request_context)


# don't know if uses model functions
def join_event(request, group_slug, event_id):
    if request.user.is_authenticated():
        if Event.objects.filter(id=event_id).exists():
            event = Event.objects.get(id=event_id)
            event.join(request.user.pk)
            return HttpResponse(status=200)
    return HttpResponse(status=401)


# don't know if uses model functions
def leave_event(request, group_slug, event_id):
    if request.user.is_authenticated():
        if Event.objects.filter(id=event_id).exists():
            event = Event.objects.get(id=event_id)
            event.leave(request.user.pk)
            return HttpResponse(status=200)
    return HttpResponse(status=401)
