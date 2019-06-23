from sly.apps.shrink.models import SlyUrl
from rest_framework import serializers

class SlyUrlSerializer(serializers.ModelSerializer):
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
			short_url.shortCode = self.generate_shortcode(short_url.id)
			short_url.save()
		else:
			short_url = SlyUrl(longUrl=long_url, shortCode=short_code)
			short_url.save()

		return short_url

	def generate_shortcode(self, id):
		'''
		Generate urls shortcode
		'''
		import string
		characters = string.digits+string.uppercase+string.lowercase
		base = len(characters)
		ret = []

		while id > 0:
			val = id % base
			ret.append(characters[val])
			id = id // base
		
		return "".join(ret[::-1])
