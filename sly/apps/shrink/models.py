from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


# Create your models here.
class SlyUrl(models.Model):
	'''Model that saves Url info to be shortened'''
	created_by = models.ForeignKey(User, related_name="slyurls", null=True, blank=True, on_delete=models.CASCADE)
	longUrl = models.URLField(max_length=300)
	shortCode = models.CharField(max_length=50, blank=True, unique=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.longUrl

	def get_short_url(self):
		'''get the shortcode url'''
		return reverse('shorturl', kwargs={'shortcode': self.shortCode})
		


