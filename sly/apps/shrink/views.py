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
				created, obj = SlyUrl(longUrl = longUrl)
				obj.save()
				obj.refresh_from_db()
				obj.shortCode = self.generate_shortcode(url.id)
				obj.save()
			else:
				created, obj = SlyUrl.objects.create(longUrl=longUrl,shortCode=shortCode)
				
			if created:
				template = 'shrink/success.html'
				context = {
						'object':obj					
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



