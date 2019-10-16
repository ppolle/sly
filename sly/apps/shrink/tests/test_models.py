from django.test import TestCase
from sly.apps.shrink.models import SlyUrl
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.urlresolvers import reverse

# Create your tests here.
class SlyUrlTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='test_user',
			email='test.user@gmail.com',
			password='testPASSWORD1234')

		self.sly_url = SlyUrl.objects.create(
			long_url='http://www.celeryproject.org/docs-and-support/',
			short_code='test_short_code',
			active=True,
			created_by=self.user)

	def test_get_short_url(self):
		self.assertEqual(self.sly_url.get_short_url(), reverse('shorturl', kwargs={'shortcode':self.sly_url.short_code}))

	def test_create_auth_token_receiver(self):
		new_user = User.objects.create_user(
			username='test_user_2',
			email='test.user_2@gmail.com',
			password='testPASSWORD1234')
		
		self.assertEqual(Token.objects.all().count(), 2)
		self.assertEqual(Token.objects.filter(user=new_user).count(), 1)

	def test_create_short_url_receiver(self):
		new_sly_url = SlyUrl.objects.create(
			long_url='http://www.google.com/',
			active=True,
			created_by=self.user)
		
		self.assertTrue(new_sly_url.short_code)