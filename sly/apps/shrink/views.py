from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UrlForm, RegisterUserForm, UserAuthForm
from .models import SlyUrl

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
			longUrl = form.cleaned_data['url']
			shortCode = form.cleaned_data['short_code']

			if shortCode == '':
				url = SlyUrl(longUrl = longUrl)
				url.save()
				url.refresh_from_db()
				url.shortCode = self.generate_shortcode(url.id)
				url.save()
			else:
				url = SlyUrl.objects.create(longUrl=longUrl,shortCode=shortCode)				
			
			template = 'shrink/home/success.html'
			context = {
					'url':url					
				}

		return render(request, template, context)

	def generate_shortcode(self, id):
		'''
		Generate urls shortcode
		'''
		import string
		characters = string.digits+string.uppercase+string.lowercase
		base = len(characters)
		ret = []

		while id > 0:
			val = id % base
			ret.append(characters[val])
			id = id // base
		
		return "".join(ret[::-1])

class ShortCodeRedirectView(View):
	def get(self, request, shortcode, *args, **kwargs):
		'''
		Redirect shortcode to the correct url
		'''
	
		url_path = SlyUrl.objects.get(shortCode=shortcode)
		return redirect(url_path.longUrl)


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
			return redirect('auth')

		return render(request, 'shrink/auth/register.html', {'form':form})

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
			form.authenticate()
			

		return render(request, 'shrink/auth/auth', {'form':form})

class ProfileView(LoginRequiredMixin, View):
	'''
	Get dashboard objects
	'''
	def get():
		urls = SlyUrl.objects.filter(created_by=request.user)
		return render(request, 'shrink/home/dashboard.html', {'urls':urls})




