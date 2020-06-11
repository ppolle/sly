from .base import *
import dj_database_url
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = ['*']

SECRET_KEY = config('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}