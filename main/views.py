from django.shortcuts import render
from main.models import Movie, WatchEvent, WatchRoom
from django.template import loader, RequestContext
from scripts import populate_movies as mov_in

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

    if request.method == 'POST':
        url = request.POST.get('url')

        if url:
            # either imdb id or 'failed' or 'not a movie'
            result = mov_in.MovieToPick.make_movie(url)
            if result == 'failed' or result == 'not a movie':
                context['is_movie'] = 'no'
                context['message'] = 'Not a Movie'
            else:
                context['is_movie'] = 'yes'
                context['movie'] = Movie.objects.get(imdb_id=result)

        else:
            context['url_response'] = 'No url was entered'



    return render(request, 'add_movie.html', context,
        context_instance=RequestContext(request, processors=[global_context]))


def create_vote(request):
    user = request.user
    movie = Movie.objects.get(imdb_id=int(request.POST['imdb_id']))

    user.votes.add(movie)
    user.save()

    return HTTPResponse(status=200)


def delete_vote(request):
    user = request.user
    movie = Movie.objects.get(imdb_id=int(request.POST['imdb_id']))

    user.votes.remove(movie)
    user.save()

    return HttpResponse(status=200)


# def get_votes(request):
#     context = {}

#     if request.user.is_authenticated():
#         votes = request.user.votes.all()
#         context['votes'] = votes

#     movies = User.votes.all().order_by('title')

#     if len(movies) > 0:
#         context['movies'] = movies
#         return render(request, 'template tk.html', context)


# def user_votes(request, username=None):
#     viewing_user = User.objects.get(username=username)

#     return render(request, 'votes.html', {'viewing_user': viewing_user})
