from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UrlForm, RegisterUserForm, UserAuthForm
from .models import SlyUrl
from django.contrib import messages

# Create your views here.
class IndexView(View):
	def get(self, request, *args, **kwargs):
		'''
		Form to dispaly the index page
		'''
		form = UrlForm()
		return render(request, 'shrink/home/index.html', {'form':form})

	def post(self, request, *args, **kwargs):
		'''
		Handle inedx page post requests
		'''
		form = UrlForm(request.POST)
		template = 'shrink/home/index.html'
		context = {'form':form}

		if form.is_valid():
			long_url = form.cleaned_data['url']
			short_code = form.cleaned_data['short_code']

			if request.user.is_authenticated:
				obj = SlyUrl.objects.create(created_by=request.user, long_url = long_url, short_code=short_code)
			else:
				obj = SlyUrl.objects.create(long_url = long_url, short_code=short_code)

		messages.success(request, 'ShortUrl creation was a success')			
		return redirect('shortcode_detail', shortcode=obj.short_code)

class ShortCodeRedirectView(View):
	def get(self, request, shortcode, *args, **kwargs):
		'''
		Redirect shortcode to the correct url
		'''
		url_path = SlyUrl.objects.get(short_code=shortcode)
		if url_path.active is True:
			return redirect(url_path.long_url)
		else:
			return render(request, 'shrink/home/inactive_url.html', {'url':url_path})


class RegistrationView(View):
	'''
	Register a new user
	'''
	def get(self, request, *args, **kwargs):
		'''
		Return the user registration page
		'''
		form = RegisterUserForm()
		return render(request, 'shrink/auth/register.html', {'form':form})

	def post(self, request, *args, **kwargs):
		'''
		Register a user
		'''
		form = RegisterUserForm(request.POST)
		template = 'shrink/auth/register.html'
		
		if form.is_valid():
			form.save()

			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
			messages.success(request, 'Succesfull Registration. Now take a tour of the Sly Dashboard.')
			return redirect('dashboard', username=username)

		return render(request, template, {'form':form})

class AuthView(View):
	'''
	Authenticate a user
	'''
	def get(self, request, *args, **kwargs):
		'''
		Render the auth form
		'''
		form = UserAuthForm()
		return render(request, 'shrink/auth/auth.html', {'form':form})

	def post(self, request, *args, **kwargs):
		'''
		Handle form posting
		'''
		form = UserAuthForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)

			if user is not None:
				login(request, user)
				messages.success(request, 'Welcome back {0} {1}'.format(user.first_name.capitalize(), user.last_name.capitalize()))
				return redirect('dashboard', username=user.username)

			else:
				messages.error(request, 'Wrong username/password combination. Please try again.')
				return redirect('auth')
			
		return render(request, 'shrink/auth/auth.html', {'form':form})

class ProfileView(LoginRequiredMixin, View):
	'''
	Get dashboard objects
	'''
	def get(self, request, *args, **kwargs):
		if request.user.username != kwargs['username']:
			return redirect('dashboard', username=request.user.username)
		else:
			from rest_framework.authtoken.models import Token
			try:
				obj = Token.objects.get(user=request.user)
			except ObjectDoesNotExist:
				obj = Token.objects.create(user=request.user)

			return render(request, 'shrink/home/dashboard.html', {'obj':obj})

class RegenerateTokenView(LoginRequiredMixin, View):
	'''
	Regenerate Authentication Token
	'''
	def get(self, request, *args, **kwargs):
		from rest_framework.authtoken.models import Token
		try:
			token = Token.objects.get(user=request.user)
			token.delete()
		except ObjectDoesNotExist:
			pass

		Token.objects.create(user=request.user)
		messages.success(request, 'API Authentication key succesfully regenerated')
		return redirect('dashboard', username=request.user.username)

class ShortUrlDetailView(View):
	def get(self, request, *args, **kwargs):
		'''
		Get Shortcode Details
		'''
		obj = SlyUrl.objects.get(short_code=kwargs['shortcode'])
		return render(request, 'shrink/home/success.html', {'obj':obj})






