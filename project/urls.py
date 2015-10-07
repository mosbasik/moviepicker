"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from main.views import (
    Home,
    GroupList, GroupDetails,
    EventDetails, CreateEvent,
)

urlpatterns = [
    # administrative site url
    url(r'^admin/', include(admin.site.urls)),

    # user
    url(r'^$', Home.as_view(), name='root'),
    url(r'^home/$', Home.as_view(), name='home'),

    # movies
    url(r'^movies/$', 'main.views.movies', name='movies'),
    url(r'^movies/(?P<imdb_id>tt\d+)/$', 'main.views.movie_details', name='movie_details'),
    url(r'^movies/add/$', 'main.views.add_movie', name='add_movie'),
    url(r'^create-vote/$', 'main.views.create_vote', name='vote'),
    url(r'^delete-vote/$', 'main.views.delete_vote', name='unvote'),

    # groups
    url(r'^groups/$', GroupList.as_view(), name='group_list'),
    url(r'^groups/add/$', 'main.views.create_group', name='create_group'),
    url(r'^group/(?P<group_slug>[-\w]+)/$', GroupDetails.as_view(), name='group_details'),

    # events
    url(r'^events/$', 'main.views.event_list', name='event_list'),
    url(r'^events/add/$', CreateEvent.as_view(), name='create_event'),
    url(r'^group/(?P<group_slug>[-\w]+)/event/(?P<event_id>[0-9]+)/$', EventDetails.as_view(), name='event_details'),
    url(r'^group/(?P<group_slug>[-\w]+)/event/(?P<event_id>[0-9]+)/join/$', 'main.views.join_event', name='join_event'),
    url(r'^group/(?P<group_slug>[-\w]+)/event/(?P<event_id>[0-9]+)/leave/$', 'main.views.leave_event', name='leave_event'),

    # local timezone cookie management
    url(r'^timezone/$', 'main.views.timezone', name='timezone'),

    # login and logout
    url(r'^login/$', 'main.user_auth.login', name='login'),
    url(r'^logout/$', 'main.user_auth.logout', name='logout'),

    # password reset flow
    url(r'^password/reset/$',
        auth_views.password_reset,
        {"template_name": "password_reset/password_reset_form.html"},
        name="password_reset"
        ),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {"template_name": "password_reset/password_reset_form_done.html"},
        name="password_reset_done"),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {"template_name": "password_reset/password_reset_confirm.html"},
        name="password_reset_confirm"),
    url(r'^password/reset/confirm/done/$',
        auth_views.password_reset_complete,
        {"template_name": "password_reset/password_reset_complete.html"},
        name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
