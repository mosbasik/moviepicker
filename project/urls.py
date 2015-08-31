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
from django.conf.urls import include, url
from django.contrib import admin
import django.contrib.auth.views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'main.views.front', name='front'),

    url(r'^login/$', 'main.user_auth.login', name='login'),
    url(r'^logout/$', 'main.user_auth.logout', name='logout'),

    url(r'^movies/$', 'main.views.all_movies', name='all_movies'),
    url(r'^movies/add/$', 'main.views.add_movie', name='add_movie'),
    url(r'^movies/liked/$', 'main.views.user_movies', name='user_movies'),
    url(r'^movies/search/$', 'main.views.movie_search', name='movie_search'),

    url(r'^rooms/$', 'main.views.all_rooms', name='all_rooms'),
    url(r'^rooms/add/$', 'main.views.create_room', name='create_room'),

    url(r'^events/add/$', 'main.views.create_event', name='create_event'),

    url(r'^create-vote/$', 'main.views.create_vote', name='vote'),
    url(r'^delete-vote/$', 'main.views.delete_vote', name='unvote'),

    # url(r'^get-votes/$', 'main.views.get_votes', name='get_votes'),
    # url(r'^(?P<username>\w+)/votes/$', 'main.views.user_votes', name='user_votes'),

    url(r'^password/reset/$',
        django.contrib.auth.views.password_reset,
        {"template_name": "password_reset/password_reset_form.html"},
        name="password_reset"
        ),
    url(r'^password/reset/done/$',
        django.contrib.auth.views.password_reset_done,
        {"template_name": "password_reset/password_reset_form_done.html"},
        name="password_reset_done"),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        django.contrib.auth.views.password_reset_confirm,
        {"template_name": "password_reset/password_reset_confirm.html"},
        name="password_reset_confirm"),
    url(r'^password/reset/confirm/done/$',
        django.contrib.auth.views.password_reset_complete,
        {"template_name": "password_reset/password_reset_complete.html"},
        name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
