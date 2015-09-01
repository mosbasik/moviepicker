from django.contrib import admin
from main.models import (
    Movie, Event, Group,
    Location, Viewing, LockIn,
)

admin.site.register(Movie)
admin.site.register(Event)
admin.site.register(Group)
admin.site.register(Location)
admin.site.register(Viewing)
admin.site.register(LockIn)
