"""
Django settings for vrautotest project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from pymongo import MongoClient
from boto import config as botoconfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Setup a database connection to be used in the rest of the code
DB_HOST = os.environ.get('DB_HOST', 'localhost:27017')
client = MongoClient(DB_HOST)
DB_NAME = os.environ.get('DB_NAME', 'autotest')
db1 = client[DB_NAME]
if 'DB_USER' in os.environ:
    db1.authenticate(os.environ.get('DB_USER'), os.environ.get('DB_PASSWORD'))
on_aws = True #"ON_AWS" in os.environ

if on_aws:
    if not botoconfig.has_section('Credentials'):
        botoconfig.add_section('Credentials')
    if not botoconfig.has_option('Credentials', 'aws_access_key_id'):
        botoconfig.set('Credentials', 'aws_access_key_id',
                       os.environ.get('AWS_KEY'))
    if not botoconfig.has_option('Credentials', 'aws_secret_access_key'):
        botoconfig.set('Credentials', 'aws_secret_access_key',
                        os.environ.get('AWS_SECRET'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z%h7pr=_$j%^l54+xcjco8e+*%y)%j7q^&0w_+j8nfsh=ra_n('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'vrapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vrautotest.urls'

WSGI_APPLICATION = 'vrautotest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
	#os.path.join(BASE_DIR, "static"),
	#'/var/www/static/',
)
STATIC_ROOT = os.path.join(BASE_DIR,'../../static-files/static')

