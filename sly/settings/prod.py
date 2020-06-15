from .base import *
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = config('SLY_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('SLY_DB_NAME'),
        'USER': config('SLY_DB_USER'),
        'PASSWORD':config('SLY_DB_PASS'),
    }
}