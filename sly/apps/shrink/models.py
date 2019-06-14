from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SlyUrl(models.Model):
	'''Model that saves Url info to be shortened'''
	url = models.CharField(max_length=300)
	short_code = models.CharField(max_length=50, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.url

	def encode(self, url):
		'''shorten a url link'''
		pass

	def decode(self, url):
		'''change a url back to original url'''
		pass

