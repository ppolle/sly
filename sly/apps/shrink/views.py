from django.shortcuts import render, redirect
from .forms import UrlForm
from .models import SlyUrl

# Create your views here.
def index(request):
	'''
	Method that displays shortens links
	'''
	if request == 'POST':
		form = UrlForm(request.POST)
		if form.is_valid():
			longUrl = form.cleaned_data['url']
			url = SlyUrl(url = longUrl)
			url.save()
			
			url.refresh_from_db()
			url.short_code = SlyUrl.encode(url.id)
			url.save()
			
			return redirect('index')
	else:
		form = UrlForm()

	return render(request, 'shrink/index.html', {'form':form})

