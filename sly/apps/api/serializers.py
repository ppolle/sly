from sly.apps.shrink.models import SlyUrl
from rest_framework import serializers

class SlyUrlSerializer(serializers.ModelSerializer):
	class Meta:
		model = SlyUrl
		fields = ("longUrl", "shortCode", "timestamp")
