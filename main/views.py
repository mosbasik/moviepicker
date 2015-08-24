from django.shortcuts import render
from main.models import Movie, WatchEvent, WatchRoom

import user_auth


def front(request):
    context = {}

    return render(request, 'index.html', context)
