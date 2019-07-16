from django.test import TestCase
from django.core.urlresolvers import reverse
from sly.apps.shrink.models import SlyUrl

# Create your tests here.
class IndexViewTests(TestCase):
	def test_short_code_creation_with_both_fields_provided(self):
		'''
		Test a shortcode can be created with both fields
		'''
		data = {'url':'http://www.celeryproject.org/docs-and-support/',
				'short_code':'test'
				}

		url = reverse('index')
		response = self.client.post(url, data, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(SlyUrl.objects.all().count(), 1)
		self.assertContains(response, 'Your shortcode has been succesfully created as shown below')
		self.assertRedirects(response, reverse('shortcode_detail', kwargs={'shortcode': 'test'}))

	def test_short_code_creation_with_only_long_url_provided(self):
		'''
		Test a shortcode is created when only a long url is provided
		'''
		data = {'url':'http://www.celeryproject.org/docs-and-support/'
				}

		url = reverse('index')
		response = self.client.post(url, data, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(SlyUrl.objects.all().count(), 1)
		self.assertContains(response, 'Your shortcode has been succesfully created as shown below')
		self.assertRedirects(response, reverse('shortcode_detail', kwargs={'shortcode': SlyUrl.objects.get(long_url=data['url']).short_code}))


	def test_authenticated_users_can_create_a_shortcode(self):
		'''
		Test a logged in user can create a shortcode
		'''
		pass

	def test_unauthenticated_user_can_create_a_shortcode(self):
		'''
		Test unauthenticated users can create a shortcode
		'''
		pass

class ShortCodeRedirectViewTests(TestCase):
	def test_redirection_passes_if_status_active(self):
		'''
		Test succesful redirection if status is active
		'''
		obj = SlyUrl.objects.create(short_code='test',long_url='https://www.google.com/')
		url = reverse('shorturl', kwargs={'shortcode':obj.short_code})
		response = self.client.get(url)
		
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], obj.long_url)
		
	def test_redirection_fail_if_status_inactive(self):
		'''
		test unsuccesfull redirection if status is inactive
		'''
		obj = SlyUrl.objects.create(short_code='test',long_url='http://www.celeryproject.org/docs-and-support/',active=False)
		url = reverse('shorturl', kwargs={'shortcode':obj.short_code})
		response = self.client.get(url, follow=True)
		
		self.assertTrue(response.status_code, 200)
		self.assertContains(response, 'Kindly contact the Url owner for further details')

