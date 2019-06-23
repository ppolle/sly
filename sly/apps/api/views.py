from sly.apps.shrink.models import SlyUrl
from .serializers import SlyUrlSerializer
from rest_framework import generics

class ShortCodeList(generics.ListCreateAPIView):
	"""
	Create a shortcode Url or list shortcode urls
	"""
	queryset = SlyUrl.objects.all()
	serializer_class = SlyUrlSerializer

class ShortCodeDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update and delete shortcode model instances
	"""
	queryset = SlyUrl.objects.all()
	serializer_class = SlyUrlSerializer
	lookup_field = 'shortCode'
