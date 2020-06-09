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
	current_site = str(Site.objects.get_current())
	incoming_site = extract_domain(value).lower().strip()

	if current_site != incoming_site:
		return value
	else:
		raise ValidationError("You cannot shorten a URL from this site")

def extract_domain(value):
	import tldextract
	uri = tldextract.extract(value).registered_domain
	return uri
