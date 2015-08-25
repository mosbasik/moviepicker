from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm


def login(request):
    if request.user.is_authenticated():
            return redirect('front')

    context = {'user_create_form': UserCreationForm()}

    if request.method == 'POST':

        if request.POST['type'] == 'login':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)

                    if request.user.is_authenticated():
                        return redirect('front')
                else:
                    context['error'] = 'Your account has been disabled'
                    return render(request, 'login.html', context)

            else:
                context['error'] = 'invalid username or password'
                return render(request, 'login.html', context)

        else:
            full_user_create_form = UserCreationForm(request.POST)

            if full_user_create_form.is_valid():

                user = full_user_create_form.save()
                user.email = request.POST['email']
                user.save()

                # group = Group.objects.get(name='users')
                # group.user_set.add(user)

                user = authenticate(username=user.username, password=request.POST['password1'])
                auth_login(request, user)

                return redirect('front')
            else:
                context['user_create_form'] = full_user_create_form
                context['error_on_create'] = True

    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')
