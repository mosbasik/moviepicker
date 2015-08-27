from django import forms
from main.models import Movie, WatchEvent, WatchRoom


class SearchMovieForm(forms.Form):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput,
    )