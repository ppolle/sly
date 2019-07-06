from django.conf.urls import url
from sly.apps.api.views import ShortCodeList, ShortCodeDetail

urlpatterns = [
	url(r'shortcode/$', ShortCodeList.as_view()),
	url(r'shortcode/(?P<shortcode>[\w-]+)$', ShortCodeDetail.as_view()),

]
