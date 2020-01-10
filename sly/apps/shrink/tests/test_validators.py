from django.test import TestCase
from django.core.exceptions import ValidationError
from sly.apps.shrink.validators import validate_url

class ValidateUrlTests(TestCase):
	def test_validate_url(self):
		url = 'blah.blah'
		self.assertRaises(ValidationError, validate_url, url)