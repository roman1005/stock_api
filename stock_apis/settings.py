"""
Django settings for stock_apis project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""


import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0)2o46@shf#12=v9%poyuwrs4571skicp3tq_pa7!x902e4+80'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

'''
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
'''
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock_apis_BE',
    'rest_framework',
    #'django_celery_results',
    #'django_celery_beat',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'stock_apis_BE.admin.SafelistPermission'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

REST_SAFE_LIST_IPS = [
    '107.23.255.128',
    '107.23.255.129',
    '107.23.255.131',
    '107.23.255.132',
    '107.23.255.133',
    '107.23.255.134',
    '107.23.255.135',
    '107.23.255.137',
    '107.23.255.138',
    '107.23.255.139',
    '107.23.255.140',
    '107.23.255.141',
    '107.23.255.142',
    '107.23.255.143',
    '107.23.255.144',
    '107.23.255.145',
    '107.23.255.146',
    '107.23.255.147',
    '107.23.255.148',
    '107.23.255.149',
    '107.23.255.150',
    '107.23.255.151',
    '107.23.255.152',
    '107.23.255.153',
    '107.23.255.154',
    '107.23.255.155',
    '107.23.255.156',
    '107.23.255.157',
    '107.23.255.158',
    '107.23.255.159',
    '35.162.152.183',
    '52.38.28.241',
    '52.35.67.149',
    '54.149.215.237',
    '13.127.146.34',
    '13.127.207.241',
    '13.232.235.243',
    '13.233.81.143',
    '13.112.233.15',
    '54.250.57.56',
    '18.182.156.77',
    '52.194.200.157',
    '3.120.160.95',
    '18.184.214.33',
    '18.197.117.10',
    '3.121.144.151',
    '13.239.156.114',
    '13.238.1.253',
    '13.54.58.4',
    '54.153.234.158',
    '18.228.167.221',
    '18.228.209.157',
    '18.228.209.53',
    '18.228.69.72',
    '13.228.169.5',
    '3.0.35.31',
    '3.1.111.112',
    '52.220.50.179',
    '34.250.225.89',
    '52.30.208.221',
    '63.34.177.151',
    '63.35.2.11'
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

ROOT_URLCONF = 'stock_apis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'stock_apis_BE/templates')],
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

WSGI_APPLICATION = 'stock_apis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'articles',
        'USER': 'root',
        'PASSWORD': 'r0man2001',
        'HOST': 'localhost',
        'PORT': '3306',
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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
