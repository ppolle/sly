from django.test import TestCase, RequestFactory
Ffrom django.core.urlresolvers import reverse
from sly.apps.shrink.models import SlyUrl
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from sly.apps.shrink.views import IndexView
from django.utils.http import urlencode

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
		response = IndexView.as_view()
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

class RegistrationViewTests(CreateObjects, TestCase):
	def test_user_creation_with_valid_arguments(self):
		url = reverse('register')
		data = {'first_name':'Test',
				'last_name':'User',
				'email':'test.user@gmail.com',
				'password1':'testPASSWORD1234',
				'password2':'testPASSWORD1234',
				'username':'test_user'}
		response = self.client.post(url, data, follow=True)

		self.assertEqual(User.objects.all().count(), 1)
		self.assertRedirects(response, reverse('dashboard', kwargs={'username':data['username']}))
		self.assertContains(response, 'Succesfull Registration. Now take a tour of the Sly Dashboard.')

	def test_user_creation_with_different_passwords(self):
		url = reverse('register')
		data = {'first_name':'Test',
				'last_name':'User',
				'email':'test.user@gmail.com',
				'password1':'testPASSWORD1234',
				'password2':'testPASSWORD123',
				'username':'test_user'}
		response = self.client.post(url, data, follow=True)

		self.assertNotEqual(User.objects.all().count(), 1)
		self.assertContains(response, "The two password fields didn&#39;t match")

	def test_user_creation_with_already_existing_username(self):
		user = self.create_user()

		url = reverse('register')
		data = {'first_name':'Test',
		'last_name':'User',
		'email':'test.user@gmail.com',
		'password1':'testPASSWORD1234',
		'password2':'testPASSWORD1234',
		'username':'test_user'}

		response = self.client.post(url, data, follow=True)

		self.assertEqual(User.objects.all().count(), 1)
		self.assertContains(response, "A user with that username already exists.")

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

class ProfileViewTests(CreateObjects, TestCase):
	def test_denying_access_to_wrong_user(self):
		user = self.create_user()
		user1 = User.objects.create_user(
			username='tester',
			email='tester@gmail.com',
			password='testPASSWORD1234'
			)
		self.client.login(username=user.username, password='testPASSWORD1234')

		url = reverse('dashboard', kwargs={'username':user1.username})
		response = self.client.get(url, follow=True)

		self.assertRedirects(response, reverse('dashboard', kwargs={'username':user.username}))

	def test_denying_access_to_unauthenticated_users(self):
		user = self.create_user()

		url = reverse('dashboard', kwargs={'username':user.username})
		login_url = reverse('auth') + '?' + urlencode({'next': url})
		response = self.client.get(login_url, follow=True)

		self.assertRedirects(response, reverse('dashboard', kwargs={'username':user.username}), 302)

class RegenerateTokenViewTests(CreateObjects, TestCase):
	def test_token_regeneratin(self):
		'''
		Test a token is regenerated
		'''
		user = self.create_user()
		self.client.login(username=user.username, password='testPASSWORD1234')
		url = reverse('regenerate-token')

		response = self.client.get(url, follow=True)

		self.assertRedirects(response, reverse('dashboard', kwargs={'username':user.username}))
		self.assertContains(response, 'API Authentication key succesfully regenerated')
		self.client.logout()

class ShortUrlDetailViewTests(TestCase):
	def test_short_url_page_redirects(self):
		short_url = SlyUrl.objects.create(long_url='https://www.google.com/',short_code='test')
		url = reverse('shortcode_detail', kwargs={'shortcode':short_url.short_code})
		response = self.client.get(url, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Your shortcode has been succesfully created as shown below')

class DeleteShortCodeViewTests(TestCase):
	def test_short_code_delete(self):
		short_url1 = SlyUrl.objects.create(long_url='https://www.google.com/')
		short_url2 = SlyUrl.objects.create(long_url='https://www.facebook.com/')

		url = reverse('shortcode_delete', kwargs={'shortcode':short_url1.short_code})
		response = self.client.get(url, follow=True)

		self.assertEqual(SlyUrl.objects.all().count(), 1)
		self.assertContains(response, 'Shortcode succesfully deleted')

class ChangeShortUrlStatusViewTests(TestCase):
	def test_change_url_status_to_inactive(self):
		short_url1 = SlyUrl.objects.create(long_url='https://www.google.com/')
		url = reverse('shortcode_change_status', kwargs={'shortcode':short_url1.short_code})
		response = self.client.get(url, follow=True)

		# self.assertEqual(short_url1.active, False)
		self.assertRedirects(response, reverse('shortcode_detail', kwargs={'shortcode':short_url1.short_code}))
		self.assertContains(response, 'ShortUrl status succesfully changed')

	def test_change_url_status_to_active(self):
		short_url1 = SlyUrl.objects.create(long_url='https://www.google.com/', active=False)
		url = reverse('shortcode_change_status', kwargs={'shortcode':short_url1.short_code})
		response = self.client.get(url, follow=True)

		# self.assertEqual(short_url1.active, True)
		self.assertRedirects(response, reverse('shortcode_detail', kwargs={'shortcode':short_url1.short_code}))
		self.assertContains(response, 'ShortUrl status succesfully changed')
