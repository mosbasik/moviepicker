from django.db.models import Count

from main.models import Movie


def get_voted_movie_qs(user_qs,
                       order_by=['-num_votes'],
                       include_unvoted=False):
    '''
    Given a queryset of User objects, returns a queryset of Movie objects each
    annotated with the number of votes it has in the User queryset.  By
    default, is ordered from most to least votes.  To change the ordering, pass
    a list of fields to order on.  The field "num_votes" can be used to order
    by votes. "
    '''

    if include_unvoted:
        movies = Movie.objects.all()
    else:
        movies = Movie.objects.filter(voters__in=user_qs)

    movies = movies.annotate(num_votes=Count('voters'))
    movies = movies.order_by(*order_by)

    return movies
