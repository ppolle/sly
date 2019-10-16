from django.test import TestCase
from sly.apps.shrink.utils import generate_shortcode

class GenerateShortCodeTests(TestCase):
	def test_generate_short_code(self):
		short_code = generate_shortcode(100)
		self.assertEqual(short_code, '1c')