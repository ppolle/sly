from sly.apps.shrink.models import SlyUrl
from .serializers import SlyUrlSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class ShortCodeList(generics.ListCreateAPIView):
	"""
	Create a shortcode Url or list shortcode urls
	"""
	queryset = SlyUrl.objects.all()
	serializer_class = SlyUrlSerializer

	def get_queryset(self):
		user = self.request.user
		return SlyUrl.objects.filter(created_by=user)

class ShortCodeDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update and delete shortcode model instances
	"""
	queryset = SlyUrl.objects.all()
	serializer_class = SlyUrlSerializer
	lookup_field = 'shortCode'
	lookup_url_kwarg = 'shortcode'

