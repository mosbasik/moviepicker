from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
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

    group = forms.ModelChoiceField(
        queryset=Group.objects.all(),   # TODO - Filter this based on the user's groups
        required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    # This is a stock overflow solutions for passing the user to the form
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('user', None)
    #     super(EventCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['group'].queryset = User.objects.filter(pk=user.id)

    # def clean(self):
    #     print self.request.user

    class Meta:
        model = Event
        fields = ['name', 'date_and_time', 'description', 'group']
    #     widgets = {
    #         'datetime': DateTimeWidget(
    #             # attrs={'class': 'form-control'},
    #             usel10n=True,
    #             bootstrap_version=3)
    #         }


class LocationForm(forms.ModelForm):

    text = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'placeholder': 'Type the location here'}))

    class Meta:
        model = Location
        fields = ['text']
