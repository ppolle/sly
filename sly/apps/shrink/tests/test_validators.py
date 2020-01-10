from django.test import TestCase
from django.core.exceptions import ValidationError
from sly.apps.shrink.validators import validate_url, extract_domain

class ValidateUrlTests(TestCase):
	def test_validate_url(self):
		url = 'blah.blah'
		self.assertRaises(ValidationError, validate_url, url)

	def test_extract_domain(self):
		url = 'https://www.youtube.com/watch?v=Btbvv9kfLqo'
		uri = extract_domain(url)
		self.assertEqual(uri, 'www.youtube.com')