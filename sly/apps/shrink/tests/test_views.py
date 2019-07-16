from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from sly.apps.shrink.models import SlyUrl
from django.contrib.auth.models import User
from sly.apps.shrink.views import IndexView

# Create your tests here.
class CreateObjects:
	def create_user(self):
		'''
		Create a user object and log it in
		'''
		user = User.objects.create_user(
			username='test_user',
			email='test.user@gmail.com',
			password='testPASSWORD1234')

		return user

class IndexViewTests(CreateObjects, TestCase):
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
		user = self.create_user()
		# self.client.login(username=user.username, password=user.password)

		data = {'url':'http://www.celeryproject.org/docs-and-support/',
		'short_code':'test'
		}

		url = reverse('index')
		request = RequestFactory().post(url, data=data)
		# request.user = user
		response = IndexView.as_view(request)
		# response = self.client.post(url, data, follow=True)
		obj = SlyUrl.objects.get(short_code=data['short_code'])

		self.assertEqual(obj.created_by, user)

		self.client.logout()
		
	def test_unauthenticated_user_can_create_a_shortcode(self):
		'''
		Test unauthenticated users can create a shortcode
		'''
		data = {'url':'http://www.celeryproject.org/docs-and-support/',
		'short_code':'test'
		}

		url = reverse('index')
		response = self.client.post(url, data, follow=True)
		obj = SlyUrl.objects.get(short_code=data['short_code'])

		self.assertEqual(obj.created_by, None)

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

class RegistrationViewTests(TestCase):
	pass

class AuthViewTests(CreateObjects, TestCase):
	def test_authetication_with_correct_details(self):
		'''
		test user authetication
		'''
		user = self.create_user()
		data = {'username':user.username,
		'password1':'testPASSWORD1234'}

		url = reverse('auth')
		response = self.client.post(url, data, follow=True)

		self.assertRedirects(response, reverse('dashboard', kwargs={'username':user.username}))
		self.assertContains(response, 'Welcome back {}'.format(user.first_name.capitalize(), user.last_name.capitalize()))

	def test_authentication_with_incorrect_password(self):
		'''
		Test user authentication with
		'''
		user = self.create_user()
		data = {'username':user.username,
				'password1':'blahblah'}

		url = reverse('auth')
		response= self.client.post(url, data, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Wrong username/password combination. Please try again.')

class ProfileViewTests(TestCase):
	pass

class RegenerateTokenViewTests(TestCase):
	pass

class ShortUrlDetailViewTests(TestCase):
	pass

class DeleteShortCodeViewTests(TestCase):
	pass

class ChangeShortUrlStatusViewTests(TestCase):
	pass
