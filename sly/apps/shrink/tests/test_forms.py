from django.test import TestCase
from sly.apps.shrink.forms import UrlForm, RegisterUserForm, UserAuthForm

# Create your tests here.
class UrlFormTests(TestCase):
	def test_valid_form(self):
		data = {
		'url': 'https://www.nation.co.ke/lifestyle/1190-1190-5p56avz/index.html',
		'short_code':'weifbwie'
		}
		form = UrlForm(data=data)
	
		self.assertTrue(form.is_valid())

	def test_form_valid_without_short_code_field(self):
		data = {
		'url':'https://www.nation.co.ke/lifestyle/1190-1190-5p56avz/index.html'
		}
		form = UrlForm(data=data)

		self.assertTrue(form.is_valid())

	def test_form_invalid(self):
		data = {
		'short_code':'test'
		}
		form = UrlForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertTrue(field, error)

		self.assertFalse(form.is_valid())

	def test_invalid_url(self):
		data = {
		'url':'abc'
		}
		form = UrlForm(data=data)
		if form.errors.items():
			field , error = form.errors.items()[0]
			self.assertEqual(error[0], "This field has to be a proper URL")

		self.assertFalse(form.is_valid())

	def test_ommit_own_url(self):
		data = {
		'url':'http://localhost:8000/'
		}
		form = UrlForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertEqual(error[0], "You cannot shorten a URL from this site")

		self.assertFalse(form.is_valid)

class UserAuthFormTests(TestCase):
	def test_valid_form(self):
		data = {
		'username':'ppolle',
		'password1':'password'
		}
		form = UserAuthForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertTrue(field, error)
		self.assertTrue(form.is_valid())
		

	def test_invalid_form(self):
		data = {
		'username':'ppolle'}
		form = UserAuthForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertTrue(field, error)
		self.assertFalse(form.is_valid())

class RegisterUserFormTests(TestCase):
	def test_form_valid(self):
		data = {'first_name':'Peter',
				'last_name':'Polle',
				'email':'peterpolle@gmail.com',
				'password1':'iamTHEBIGBOSS1234',
				'password2':'iamTHEBIGBOSS1234',
				'username':'ppolle'
				}
		form = RegisterUserForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertEqual(field, error)

		self.assertTrue(form.is_valid())

	def test_form_invalid(self):
		data = {'first_name':'Peter',
				'last_name':'Polle',
				'email':'peter@polle@gmail.com',
				'password1':'iamTHEBIGBOSS1234',
				'password2':'iamTHEBIGBOSS1234',
				}
		form = RegisterUserForm(data=data)
		self.assertFalse(form.is_valid())

	def test_password1_must_be_equal_to_password2(self):
		data = {'first_name':'Peter',
		'last_name':'Polle',
		'email':'peter@polle@gmail.com',
		'password1':'iamTHEBIGBOSS1234',
		'password2':'iamTHEBIGBOSS123',
		'username':'ppolle'
		}
		form = RegisterUserForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertEqual(error[0], "The two password fields didn't match.")

		self.assertFalse(form.is_valid())


