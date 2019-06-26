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

		# def save(self):
	# 	'''
	# 	Save a url object
	# 	'''
	# 	url = self.cleaned_data['url']
	# 	short_code = self.cleaned_data['short_code']

	# 	if short_code:
	# 		SlyUrl.objects.create(longUrl=url, shortCode=short_code)
	# 	else:
	# 		SlyUrl.objects.create(longUrl=longUrl)

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
	
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

	def save(self):
		'''
		Method to create a user
		'''
		first_name = self.cleaned_data['first_name']
		last_name = self.cleaned_data['last_name']
		email = self.cleaned_data['email']
		password= self.cleaned_data['password1']

		user = User.objects.create_user(email=email, first_name=first_name, last_name=last_name,
			password=password)
		user.save()

class UserAuthForm(forms.ModelForm):
	'''
	Form to autheticate users
	'''
	email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
		widget=forms.TextInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	password1 = forms.CharField(label="Password", max_length=300, required=True,
		widget=forms.PasswordInput(attrs={'autofocus': 'autofocus', 'class': 'form-control'}))
	
	class Meta:
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
			#redirect to the profile page

		else:
			#redirect to the login page
			pass


