from django.conf.urls import url

from .views import IndexView, ShortCodeRedirect

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<shortcode>[\w-]+)/$', ShortCodeRedirect.as_view(), name='shorturl'),
]
