from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

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