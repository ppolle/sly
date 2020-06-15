from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = config('SLY_SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('SLY_DB_NAME'),
        'USER': config('SLY_DB_USER'),
        'PASSWORD':config('SLY_DB_PASS'),
    }
}
