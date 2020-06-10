import os
import json

# Open secure files here make sure to import the
# json module and load the file to be able to
# read data if the file is json.
SECURE_FILE = os.path.abspath("/etc/django_secure/secure.json")
with open(SECURE_FILE, 'r') as secureFile:
    config = json.load(secureFile)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost', '192.168.8.100', '192.168.8.101',
    '192.168.8.102', '192.168.8.103'
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My installed apps. You can just write the
    # name of the app like 'userapp'
    'userapp.apps.UserappConfig',
    'blogapp.apps.BlogappConfig',
    # Third party installed apps
    'django_countries',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'uss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# currently making use of mysql database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': '/etc/mysql/my.cnf'
        }
    }
}

# Cache setting
# Make sure to install the neccesary bindings

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

# My custom user model
# if you are making use of a custom user model
AUTH_USER_MODEL = 'userapp.User'

# URLS to redirect to on successful actions
LOGIN_REDIRECT_URL = 'sign-in'
# LOGOUT_REDIRECT_URL = 'sign-in'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/static/'
# if your static folder is in the same level directory
# as the app, use this intead
STATIC_ROOT = ''
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
# else use this
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


# Media files (Images, Files, and Others)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# My Email backend settings
EMAIL_BACKEND = config['BACKENDS']['CONSOLE']
EMAIL_HOST = config['HOST']
EMAIL_PORT = config['TLS_PORT']
EMAIL_HOST_USER = config['USER']
EMAIL_HOST_PASSWORD = config['PASSWORD']
EMAIL_USE_TLS = config['TLS']
# EMAIL_USE_SSL =
DEFAULT_FROM_EMAIL = config['USER']
