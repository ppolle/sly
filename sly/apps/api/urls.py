from django.conf.urls import url
# # from sly.apps.api.views import ShortCodeList

# # urlpatterns = [
# # 	url(r'shortcode/$', ShortCodeList.as_view())
# ]

# from django.conf.urls import url

from sly.apps.shrink.views import IndexView, ShortCodeRedirect

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<shortcode>[\w-]+)/$', ShortCodeRedirect.as_view(), name='shorturl'),
]
