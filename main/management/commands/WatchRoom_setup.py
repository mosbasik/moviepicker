from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from main.models import Movie, WatchEvent, WatchRoom


class Command(BaseCommand):

    def handle(self, *args, **options):
        room, created = WatchRoom.objects.get_or_create(name='Universal')
        room.description = 'Welcome to the World'

        room.save()
