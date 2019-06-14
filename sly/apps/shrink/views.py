from django.shortcuts import render, redirect
from .forms import UrlForm
from .models import SlyUrl

# Create your views here.
def index(request):
	'''
	Method that displays shortens links
	'''
	if request.method == 'POST':
		form = UrlForm(request.POST)
		if form.is_valid():
			longUrl = form.cleaned_data['url']
			shortCode = form.cleaned_data['short_code']

			if shortCode is None:
				url = SlyUrl.objects.create(longUrl = longUrl)		
			else:
				url = SlyUrl.objects.create(longUrl=longUrl,shortCode=shortCode)
			
			return render(request, 'shrink/success.html', {'shortUrl':url.shortCode})

	else:
		form = UrlForm()

	return render(request, 'shrink/index.html', {'form':form})

