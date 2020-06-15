from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = config('SECRET_KEY')

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD':config('DB_PASS'),
    }
}
