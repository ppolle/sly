from django.conf.urls import url
from sly.apps.api.views import ShortCodeList

urlpatterns = [
	url(r'shortcode/$', ShortCodeList.as_view())
]
