from django.conf.urls import url

from .  import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<shortcode>[\w-]+)/$', views.ShortCodeRedirectView.as_view(), name='shorturl'),
	url(r'^auth/register$', views.RegistrationView.as_view(), name='register'),
]
