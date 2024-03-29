"""
Django settings for news_app project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from elasticsearch_dsl import connections
from requests.auth import HTTPBasicAuth
from decouple import config
from news_app.get_env_values import get_secret
from urllib.parse import quote_plus as urlquote

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = get_secret('SECRET_KEY')
DEBUG = get_secret('DEBUG')

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django_crontab',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'UserAuth',
    'newshub',
    'newscollector',
    'django_celery_beat',
    'branches',

    #Social Auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter_oauth2',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'news_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR,'templates'],
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

WSGI_APPLICATION = 'news_app.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT'),         
    }
}



ELASTICSEARCH_DSL = {
'default': {
        'hosts': 'https://54.215.27.92:9200',
        'http_auth': (get_secret("ELASTIC_USERNAME"), get_secret("ELASTIC_PASSWD")),
        'verify_certs': False
    },
}
connections.configure(**ELASTICSEARCH_DSL)


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/images/'

MEDIA_ROOT = 'images/'

# SOCIAL_AUTH_JSONFIELD_ENABLED = True


AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SITE_ID = 1  

ACCOUNT_EMAIL_VERIFICATION = 'none'

SOCIALACCOUNT_LOGIN_ON_GET=True

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'APP': {
            # 'client_id': 'your_facebook_client_id',
            # 'secret': 'your_facebook_client_secret',
            'client_id': f'{get_secret("FACEBOOK_CLIENT_ID")}',
            'secret': f'{get_secret("FACEBOOK_CLIENT_SECRET")}',
        },
        'LOCALE_FUNC': lambda request: 'en_US'
    },
    'google': {
        'APP': {
            'client_id': f'{get_secret("GOOGLE_CLIENT_ID")}',
            'secret': f'{get_secret("GOOGLE_CLIENT_SECRET")}',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    },
    'twitter_oauth2': {
        'APP': {
            'client_id': f'{get_secret("TWITTER_CLIENT_ID")}',
            'secret': f'{get_secret("TWITTER_CLIENT_SECRET")}',
        }
    }
}

# SMTP config for gmail 
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER=f'{get_secret("HOST_EMAIL_ID")}'
EMAIL_HOST_PASSWORD=f'{get_secret("HOST_EMAIL_PASSWORD")}'
EMAIL_USE_TLS=True
EMAIL_PORT=587



CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"

# CELERY_BROKER_URL = "redis://127.0.0.1:6379"
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ["application/json"]
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Asia/Kolkata'


CSRF_TRUSTED_ORIGINS=['https://crene.com',]

CRONJOBS = [
    ('0 0 * * *', 'newscollector.task.news_scrapper'),
]

# Store msg when redirecting to another url
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'


# Custom adapter for social auth 
SOCIALACCOUNT_ADAPTER = 'UserAuth.adapters.MySocialAccountAdapter'

#CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'


# aws config for S3 bucket
AWS_ACCESS_KEY_ID = get_secret('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = get_secret('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = get_secret('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = 's3v4',
AWS_S3_REGION_NAME = get_secret('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERITY = True
AWS_QUERYSTRING_AUTH = False
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_PUBLIC_MEDIA_LOCATION = 'branchimages/'