import os, sys

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from main.models import WatchRoom
from main.forms import GroupCreationForm


def create_group(request, user):

    context = {}

    if request.method == 'POST' and request.user.is_authenticated():
        form = GroupCreationForm(request.POST)
        context['form'] = form

        if form.is_valid():
            group_exists = WatchRoom.objects.filter(name=name).exists()

            if not group_exists:
                group = WatchRoom()
                group.name = form.cleaned_data['name']
                group.description = form.cleaned_data['description']
                group.users = 'users'
                created_by = user

                group.save()
                context['group'] = group

                context['valid'] = "Group created successfully."
                return render(request, 'add_group.html', context)

            else:
                context['message'] = "Sorry, you must be a registered user to create a group."
                return 'failed'
        
        else:
            context['valid'] = "Group not created. Either you're the idiot or we are."

    else:
        form = GroupCreationForm()
        context['form'] = form

        return render(request, 'add_group.html', context)

