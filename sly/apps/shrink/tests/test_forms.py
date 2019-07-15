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
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertEqual(field, error)

		self.assertTrue(form.is_valid())

	def test_form_valid_without_short_code_field(self):
		data = {
		'url':'https://www.nation.co.ke/lifestyle/1190-1190-5p56avz/index.html'
		}
		form = UrlForm(data=data)
		if form.errors.items():
			field, error = form.errors.items()[0]
			self.assertEqual(field, error)

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


