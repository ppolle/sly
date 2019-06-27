from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .validators import validate_url


class UrlForm(forms.Form):
	'''
	Form to shorten a new url
	'''
	url = forms.CharField(label='Shorten Url', max_length=300, required=True, validators=[validate_url],
                          widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	short_code = forms.CharField(label='Custom Short Url', max_length=300, required=False, widget=forms.TextInput(
        attrs={'autofocus': 'autofocus', 'class': 'form-control'}))

class RegisterUserForm(UserCreationForm):
	'''
	Form to create a new user
	'''
	first_name = forms.CharField(label='First Name', max_length=300, required=True,
		widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	last_name = forms.CharField(label='Last Name', max_length=300, required=True,
		widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
		widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	password1 = forms.CharField(label="Password", max_length=300, required=True,
		widget=forms.PasswordInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	password2 = forms.CharField(label="Repeat Password", max_length=300, required=True,
		widget=forms.PasswordInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	username = forms.CharField(label='Last Name', max_length=300, required=True,
		widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserAuthForm(forms.ModelForm):
	'''
	Form to autheticate users
	'''
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
		widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	password1 = forms.CharField(label="Password", max_length=300, required=True,
		widget=forms.PasswordInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	
	class Meta:
		model = User
		fields =('email', 'password')

	def authenticate(self, request):
		'''
		Authenticate users
		'''
		from django.contrib.auth import authenticate, login
		from django.shortcuts import redirect

		email = self.cleaned_data['email']
		password = self.cleaned_data['password1']
		user = authenticate(request, email=email,password=password)

		if user is not None:
			login(request, user)
			return redirect('dashboard')

		else:
			#should include a message that there is a wrong username/password combination
			return redirect('auth')
	


