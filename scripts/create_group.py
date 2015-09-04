#!/usr/bin/env python
import os
import sys
import json

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

from main.models import Group
from main.forms import GroupForm


class CreateGroups():

    def create_group(request, user):

        context = {}

        if request.method == 'POST' and request.user.is_authenticated():
            form = GroupForm(request.POST)
            context['form'] = form

            if form.is_valid():
                group_exists = Group.objects.filter(name=name).exists()

                if not group_exists:
                    group = Group()
                    group.name = form.cleaned_data['name']
                    group.description = form.cleaned_data['description']
                    group.users = 'users'
                    creator = user

                    group.save()
                    context['group'] = group

                    context['valid'] = "Group created successfully."
                    return render(request, 'add_group.html', context)

                else:
                    context['message'] = "Sorry, you must be a registered user to create a group."
                    return 'failed'

            else:
                context['valid'] = "Group not created."

        else:
            form = GroupForm()
            context['form'] = form

            return render(request, 'add_group.html', context)
