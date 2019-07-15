from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .  import views

urlpatterns = [
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^auth/register/$', views.RegistrationView.as_view(), name='register'),
	url(r'^auth/login/$', views.AuthView.as_view(), name='auth'),
	url(r'^user/profile/(?P<username>[\w-]+)/$', views.ProfileView.as_view(), name='dashboard'),
	url(r'^user/logout/$', auth_views.logout, {"next_page": '/auth/login/'}, name='logout'),
	url(r'^user/regenerate-token/$', views.RegenerateTokenView.as_view(), name='regenerate-token'),
	url(r'^shortcode/(?P<shortcode>[\w-]+)/$', views.ShortUrlDetailView.as_view(), name='shortcode_detail'),
	url(r'^shortcode/delete/(?P<shortcode>[\w-]+)/$', views.DeleteShortCodeView.as_view(), name='shortcode_delete'),
	url(r'^(?P<shortcode>[\w-]+)/$', views.ShortCodeRedirectView.as_view(), name='shorturl'),
]
