from __future__ import unicode_literals

from . import utils
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


# Create your models here.
class SlyUrl(models.Model):
	'''Model that saves Url info to be shortened'''
	created_by = models.ForeignKey(User, related_name="slyurls", null=True, blank=True, on_delete=models.CASCADE)
	long_url = models.URLField(max_length=300)
	short_code = models.CharField(max_length=50, blank=True, unique=True)
	active =  models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.long_url

	class Meta:
		ordering = ['-timestamp']


	def get_short_url(self):
		'''get the shortcode url'''
		return reverse('shorturl', kwargs={'shortcode': self.short_code})

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=SlyUrl)
def create_short_url(sender, instance=None, **kwargs):
	if instance.short_code == '':
		instance.short_code = utils.generate_shortcode(instance.id)
		instance.save()

		


