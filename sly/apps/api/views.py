from sly.apps.shrink.models import SlyUrl
from .serializers import SlyUrlSerializer
from .permissions import IsCreatorOrReadOnly
from rest_framework import generics

class ShortCodeList(generics.ListCreateAPIView):
	"""
	Create a shortcode Url or list shortcode urls
	"""
	queryset = SlyUrl.objects.all()
	serializer_class = SlyUrlSerializer

	def get_queryset(self):
		user = self.request.user
		return SlyUrl.objects.filter(created_by=user)

	def perform_create(self, serializer):
		serializer.save(created_by=self.request.user, active=True)

class ShortCodeDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Retrieve, update and delete shortcode model instances
	"""
	queryset = SlyUrl.objects.all()
	serializer_class = SlyUrlSerializer
	permission_classes = (IsCreatorOrReadOnly,)
	lookup_field = 'short_code'
	lookup_url_kwarg = 'shortcode'

