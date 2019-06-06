from django import forms

class UrlForm(forms.Form):
	url = forms.CharField(label='Shorten Url', max_length=300, required=True,
                               widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
