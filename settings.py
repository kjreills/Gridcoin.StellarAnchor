"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 2.2.19.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
import logging
import seqlog

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()

SECRET_KEY = env('SECRET_KEY')

GRIDCOIN_CLIENT_ID=env('GRIDCOIN_CLIENT_ID')
GRIDCOIN_CLIENT_SECRET=env('GRIDCOIN_CLIENT_SECRET')
GRIDCOIN_API_URL=env('GRIDCOIN_API_URL')
GRIDCOIN_AUTH_URL=env('GRIDCOIN_AUTH_URL')
GRIDCOIN_AUDIENCE=env('GRIDCOIN_AUDIENCE')

ENVIRONMENT=env("ENVIRONMENT")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'server',
    'polaris',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]

POLARIS_ACTIVE_SEPS = ["sep-1", "sep-10", "sep-24"]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DBNAME'),
        'HOST': env('DBHOST'),
        'USER': env('DBUSER'),
        'PASSWORD': env('DBPASS')
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "handlers": {
        "console": {
            "class": "seqlog.structured_logging.ConsoleStructuredLogHandler",
            "level": "DEBUG"
        },
        "seq": {
            "class": "seqlog.structured_logging.SeqLogHandler",
            "server_url": env("SEQ_URL"),
            "api_key": "",
            "level": logging.INFO,
            "batch_size": 10,
            "auto_flush_timeout": 10  # seconds
        }
    },
    "loggers": {
        "integrations": {"handlers": ["console", "seq"], "propogate": False, "level": "INFO"},
        "wallet": {"handlers": ["console", "seq"], "propogate": False, "level": "INFO"},
        "polaris": {"handlers": ["console", "seq"], "propogate": False, "level": "DEBUG"},
        "django": {"handlers": ["console", "seq"], "propogate": False, "level": "INFO"},
    }
}

seqlog.set_global_log_properties(
    Environment=ENVIRONMENT
)
