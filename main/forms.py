from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.contrib.auth.models import User

from main.models import Movie, Event, Group, Location


class MovieSearchForm(forms.Form):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Movie Title',
            }
        )
    )


class GroupForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Name your group'
            }
        )
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe your group'
            }
        )
    )


class EventForm(forms.Form):

    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Name this event. We double-dog dare you.'
            }
        )
    )

    date_and_time = forms.DateTimeField(
        required=True,
        widget=DateTimeWidget(
            usel10n=True,
            options={'showMeridian': True},
            attrs={'class': 'form-control'},
            bootstrap_version=3,
            )
        )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe your event. Answer me!'
            }
        )
    )

    class Meta:
        model = Event
        fields = ['name', 'date_and_time', 'description', 'group']

    def __init__(self, user, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['group'] = forms.ModelChoiceField(
            queryset=Group.objects.filter(users=user).exclude(name='World'))


class LocationForm(forms.ModelForm):

    text = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Type the location here'}))

    class Meta:
        model = Location
        fields = ['text']


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email')

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }

    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }))

    email = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }))

    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }))

    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }))

    def clean_password2(self):
            password1 = self.cleaned_data.get('password1', None)
            password2 = self.cleaned_data.get('password2', None)
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch'
                )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
