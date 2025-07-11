"""
Django settings for th project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import django_heroku
import sys

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# service worker file
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'points/static/points/js/serviceworker.js')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# get heroku, because thats we're using to host this app
IS_HEROKU = "DYNO" in os.environ

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-og7j6bw%am%o^6$4$hcs08crjm#5@=(f+g!r-p(%4glg*fby&6'

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if '0.0.0.0:8000' in sys.argv:
    DEBUG = True
    PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'points/static/points/js/serviceworker.js')

if IS_HEROKU:
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

if '0.0.0.0:8000' not in sys.argv:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Application definition

INSTALLED_APPS = [
    'points',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # added whitenoise to allow us to serve static files to heroku
    'whitenoise.runserver_nostatic',
    # cloudinary for image hosting
    'cloudinary',
    # added pwa to allow us to use service workers
    'pwa',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # added whitenoise to allow us to serve static files to heroku
    'whitenoise.middleware.WhiteNoiseMiddleware',    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'th.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'th.wsgi.application'

# Allow to send unlimited post/get data
DATA_UPLOAD_MAX_NUMBER_FIELDS = None


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# if '0.0.0.0:8000' in sys.argv or 'testserver' in sys.argv:
if 'testserver' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'HOST': 'c3s3fim8qtlasl.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com',
            'PORT': '5432',
            'NAME': 'd6dpsveo0t27r8',
            'USER': 'udq4uc4hn8pa4k',
            'PASSWORD': 'p0f2869f7d430236d86e16a9f778c830bf432ad75fa7fda80f8aac63c3690c31a',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
        }
    }


# adding our apps users
AUTH_USER_MODEL = 'points.User'


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_TZ = True

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mbp@cgiflorida.com'
EMAIL_HOST_PASSWORD = 'zwgdlirccpsdbodw'
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# no idea why these are here, but youtube said so and it works because of it
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = '/static/'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
django_heroku.settings(locals())

# Enable WhiteNoise's GZip compression of static assets.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# login url 
LOGIN_URL = '/login'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# PWA
PWA_APP_NAME = 'Tzivos Hashem'
PWA_APP_DESCRIPTION = "CGI FLorida Tzivos Hashem"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = 'staff'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = '/staff'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/points/pngs/avatar.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/points/pngs/avatar.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/points/pngs/avatar.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'
