from django import forms
from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget
from main.models import Movie, WatchEvent, WatchRoom


class SearchMovieForm(forms.Form):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter Movie Title',
            }
        )
    )


class GroupCreationForm(forms.Form):
    name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Name your room'
            }
        )
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Describe your room'
            }
        )
    )


class EventCreationForm(forms.Form):

    event_name = forms.CharField(
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
                    attrs={'class': 'form-control'},
                    # usel10n=True,
                    bootstrap_version=3
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


    # class Meta:
    #     model = WatchEvent
    #     fields = ['event_name', 'date_and_time', 'description']
    #     widgets = {
    #         'datetime': DateTimeWidget(
    #             # attrs={'class': 'form-control'},
    #             usel10n=True,
    #             bootstrap_version=3)
    #         }