from django import forms
from .validators import validate_url


class UrlForm(forms.Form):
    url = forms.CharField(label='Shorten Url', max_length=300, required=True, validators=[validate_url]
                          widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
    short_code = forms.CharField(label='Custom Short Url', max_length=300, required=False, widget=forms.TextInput(
        attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
