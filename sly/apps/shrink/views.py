from django.shortcuts import render, redirect
from django.views.generic.base import View
from .forms import UrlForm
from .models import SlyUrl

# Create your views here.
class IndexView(View):
	def get(self, request, *args, **kwargs):
		'''
		Form to dispaly the index page
		'''
		form = UrlForm()
		return render(request, 'shrink/index.html', {'form':form})

	def post(self, request, *args, **kwargs):
		'''
		Handle inedx page post requests
		'''
		form = UrlForm(request.POST)
		template = 'shrink/index.html'
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
				created, url = SlyUrl.objects.create(longUrl=longUrl,shortCode=shortCode)
				
			
			template = 'shrink/success.html'
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

class ShortCodeRedirect(View):
	def get(self, request, shortcode, *args, **kwargs):
		'''
		Redirect shortcode to the correct url
		'''
	
		url_path = SlyUrl.objects.get(shortCode=shortcode)
		return redirect(url_path.longUrl)





