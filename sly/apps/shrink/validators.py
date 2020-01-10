from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.contrib.sites.models import Site

def validate_url(value):
	'''
	Url field validators
	'''
	url_validator = URLValidator()
	try:
		url_validator(value)
	except:
		raise ValidationError("This field has to be a proper URL")

	return value

def omit_own_domain(value):
	current_site = Site.objects.get_current()
	incoming_site = extract_domain(value).lower().strip()

	if current_site is not incoming_site:
		raise ValidationError("You cannot shorten a URL from this site")
	else:
		return value

def extract_domain(value):
	from urlparse import urlparse

	uri = urlparse(value)
	return uri.netloc
