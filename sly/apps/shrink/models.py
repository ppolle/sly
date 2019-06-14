from __future__ import unicode_literals

from django.db import models


# Create your models here.
class SlyUrl(models.Model):
	'''Model that saves Url info to be shortened'''
	longUrl = models.CharField(max_length=300)
	shortCode = models.CharField(max_length=50, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.url

	def decode(self, url):
		'''change a url back to original url'''
		pass


