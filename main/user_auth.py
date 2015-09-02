from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib.auth.forms import UserCreationForm


from main.models import Group
from main.forms import UserCreationForm


def login(request):

    # if a user is already logged in, redirect to the front page
    if request.user.is_authenticated():
            return redirect('front')

    # load a blank registration form to context in case they want to register
    context = {}
    context['user_create_form'] = UserCreationForm()
    context['next'] = request.GET.get('next', '/')

    if request.method == 'POST':

        # if the POST request was a submission of the login form
        if request.POST['type'] == 'login':

            # attempt to authenticate the user
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])

            # if the user is found in the database
            if user is not None:

                # and if the user's account is active
                if user.is_active:

                    # then log the user in and redirect to front page
                    auth_login(request, user)
                    if request.user.is_authenticated():
                        return redirect(request.POST.get('next', '/'))

                # if the user's account is not active
                else:

                    # load an error message to context and reload page
                    context['error'] = 'Your account has been disabled.'
                    return render(request, 'login.html', context)

            # if the user is not found in the database
            else:

                # load an error message to context and reload page
                context['error'] = 'Invalid username or password.'
                return render(request, 'login.html', context)

        # if the POST request was a submission of the registration form
        elif request.POST['type'] == 'create_user':

            # save a copy of the filled registration form
            filled_user_creation_form = UserCreationForm(request.POST)

            # if the filled form is valid
            if filled_user_creation_form.is_valid():

                # create a new user with the form information (the email field
                # has to be saved manually because although Django renders an
                # email field by default, it doesn't actually save it by
                # default)
                user = filled_user_creation_form.save()
                # user.email = request.POST['email']
                # user.save()

                # authenticate the new user against the database (a formality)
                user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])

                # log the new user into the site
                auth_login(request, user)

                # get the "world" group and add the new user to it
                group = Group.objects.get(name='World')
                group.users.add(user)

                # redirect user to the front page
                return redirect(request.POST.get('next', '/'))

            # if the filled form is invalid
            else:

                # load invalid form to context to be passed back for editing
                context['error_on_create'] = True
                context['user_create_form'] = filled_user_creation_form


    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')
