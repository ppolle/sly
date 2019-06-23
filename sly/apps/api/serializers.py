from sly.apps.shrink.models import SlyUrl
from rest_framework import serializers
from sly.apps.shrink.views import IndexView

class SlyUrlSerializer(serializers.ModelSerializer):

	timestamp = serializers.DateTimeField(
		format='%d.%m.%Y %H:%M',
		required=False,
		read_only=True)

	class Meta:
		model = SlyUrl
		fields = ("longUrl", "shortCode", "timestamp")

	def create(self, validated_data):
		'''
		Custom shortcode creation
		'''
		short_code = validated_data['shortCode']
		long_url = validated_data['longUrl']
		if validated_data['shortCode'] == '':
			short_url = SlyUrl(longUrl=long_url)
			short_url.save()
			short_url.refresh_from_db()
			short_url.shortCode = IndexView().generate_shortcode(short_url.id)
			short_url.save()
		else:
			short_url = SlyUrl(longUrl=long_url, shortCode=short_code)
			short_url.save()

		return short_url



