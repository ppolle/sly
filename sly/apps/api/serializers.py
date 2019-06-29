from sly.apps.shrink.models import SlyUrl
from rest_framework import serializers
from sly.apps.shrink.views import IndexView
from sly.apps.shrink.validators import validate_url

class SlyUrlSerializer(serializers.ModelSerializer):

	timestamp = serializers.DateTimeField(
		format='%d.%m.%Y %H:%M',
		required=False,
		read_only=True)

	longUrl = serializers.URLField(
		required=True,
		validators=[validate_url])

	created_by = serializers.ReadOnlyField(source='created_by.username')

	class Meta:
		model = SlyUrl
		fields = ("longUrl", "shortCode", "timestamp", "created_by")



