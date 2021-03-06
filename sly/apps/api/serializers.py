from sly.apps.shrink.models import SlyUrl
from rest_framework import serializers
from sly.apps.shrink.views import IndexView
from sly.apps.shrink.validators import validate_url, omit_own_domain, url_exists

class SlyUrlSerializer(serializers.ModelSerializer):

	timestamp = serializers.DateTimeField(
		format='%d.%m.%Y %H:%M',
		required=False,
		read_only=True)

	long_url = serializers.URLField(
		required=True,
		validators=[validate_url, omit_own_domain, url_exists])

	created_by = serializers.ReadOnlyField(source='created_by.username')

	class Meta:
		model = SlyUrl
		fields = ("long_url", "short_code", "timestamp", "created_by", 'active')



