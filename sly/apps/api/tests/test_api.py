from django.test import TestCase
from sly.apps.shrink.models import SlyUrl
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

# Create your tests here.

class ApiTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='test_user',
			email='test.user@gmail.com',
			password='testPASSWORD1234')

		self.user1 = User.objects.create_user(
			username='test_user1',
			email='test.user1@gmail.com',
			password='testPASSWORD12341')

		self.token = Token.objects.get(user=self.user)

		self.sly_url1 = SlyUrl.objects.create(
				long_url='http://www.celeryproject.org/docs-and-support/',
				short_code='test',
				created_by=self.user
			)

		self.sly_url2 = SlyUrl.objects.create(
				long_url='https://www.google.com/',
				short_code='test2',
				created_by=self.user
			)
		self.client = APIClient()

	def test_create_short_code_object(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/',
				'short_code':'test1'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 201)
		self.assertEqual(SlyUrl.objects.all().count(), 3)
		self.assertEqual(response.data['short_code'], 'test1')

	def test_create_custom_short_code(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/',
				'short_code':'test3'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data['short_code'], 'test3')
		self.assertTrue(SlyUrl.objects.get(short_code='test3'))

	def test_create_short_code_that_exists(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/',
				'short_code':'test2'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 400)
		self.assertEqual(SlyUrl.objects.all().count(), 2)
		self.assertEqual(response.data['short_code'][0], 'SlyUrl with this short code already exists.')

	def test_generate_short_code(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 201)
		self.assertEqual(SlyUrl.objects.all().count(), 3)
		self.assertTrue(response.data['short_code'])

	def test_default_short_code_status_is_True(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 201)
		self.assertEqual(SlyUrl.objects.all().count(), 3)
		self.assertEqual(response.data['active'], True)

	def test_edit_short_code_object(self):
		test_object = SlyUrl.objects.create(
				long_url='https://www.google.com/',
				short_code='test4',
				created_by=self.user
				)
		self.assertEqual(SlyUrl.objects.all().count(), 3)

		url = '/api/v1/shortcode/test4'
		data = {'active':False}
		response = self.client.patch(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(False, response.data['active'])
		self.assertEqual('test4', response.data['short_code'])

	def test_delete_short_code(self):
		test_object = SlyUrl.objects.create(
				long_url='https://www.google.com/',
				short_code='test5',
				created_by=self.user
				)
		self.assertEqual(SlyUrl.objects.all().count(), 3)

		url = '/api/v1/shortcode/test5'
		response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 204)
		self.assertEqual(SlyUrl.objects.all().count(), 2)

	def test_short_code_creation_with_invalid_url(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'invalid url',
				'short_code':'test4'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 400)
		self.assertEqual(SlyUrl.objects.all().count(), 2)
		self.assertEqual(response.data['long_url'][0], "This field has to be a proper URL")

	def test_no_token_with_sly_url(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/',
				'short_code':'test'}
		response = self.client.post(url, data)

		self.assertEqual(response.status_code, 401)
		self.assertEqual(SlyUrl.objects.all().count(), 2)

	def test_invalid_token(self):
		url = '/api/v1/shortcode/'
		data = {'long_url':'https://google.com/',
				'short_code':'test'}
		response = self.client.post(url, data, HTTP_AUTHORIZATION='Token 12356')

		self.assertEqual(response.status_code, 401)
		self.assertEqual(SlyUrl.objects.all().count(), 2)
		self.assertEqual(response.data['detail'], 'Invalid token.')

	def test_get_short_code(self):
		url = '/api/v1/shortcode/test'
		response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['short_code'], 'test')
		self.assertContains(response, 'test')

	def test_get_short_codes(self):
		url = '/api/v1/shortcode/'
		response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data[0].get('short_code'), 'test2')
		self.assertEqual(response.data[1].get('short_code'), 'test')

	def test_get_nonexistent_short_codes(self):
		url = '/api/v1/shortcode/testing_invalids'
		response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + str(self.token))

		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data['detail'], 'Not found.')

	def test_unauthorized_access_to_slyurl(self):
		token = Token.objects.get(user=self.user1)
		url = '/api/v1/shortcode/test2'
		response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + str(token))
		

		self.assertEqual(response.status_code, 403)
		self.assertEqual(response.data['detail'], 'You do not have permission to perform this action.')
		
		data = {'active':False}
		response2 = self.client.put(url, data, HTTP_AUTHORIZATION='Token ' + str(token))

		self.assertEqual(response2.status_code, 403)
		self.assertEqual(response2.data['detail'], 'You do not have permission to perform this action.')
