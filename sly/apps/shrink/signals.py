from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import SlyUrl
from .utils import *

@receiver(post_save, sender=SlyUrl)
def create_short_code(sender, instance, created, **kwargs):
	if created:
		if instance.shortCode is None:
			short_code = encode(instance.id)
			instance.shortCode = short_code
			instance.save()

