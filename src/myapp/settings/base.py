"""
Django settings for myapp project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7hhc!mriw7x$#pic$s2^bccl4ztssgn(wt_t_v7sgutzh!%9r@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(os.environ.get('DEBUG', str(False)))

ALLOWED_HOSTS = eval(os.environ.get('ALLOWED_HOSTS', '[]'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'django_extensions',

    'authentication',
]

SITE_ID = 1
AUTH_USER_MODEL = 'authentication.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myapp.urls'

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

WSGI_APPLICATION = 'myapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': eval(os.environ.get('DATABASE', 'None'))
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static_my_project')
]

STATIC_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static_cdn', 'static_root')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'static_cdn', 'media_root')

#####################
# DRF Configs
#####################
REST_FRAMEWORK = {
    # 'DEFAULT_METADATA_CLASS': None,
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'EXCEPTION_HANDLER': 'tools.rest_framework.exceptions.custom_exception_handler',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_PAGINATION_CLASS': 'tools.rest_framework.pagination.StandardResultsPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ]
}

#####################
# allauth config
#####################
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'      # choose one of "mandatory", "optional", or "none"
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
# A list of username that can’t be used by user.
ACCOUNT_USERNAME_BLACKLIST = [
    'admin', 'root', 'master', 'owner', 'ceo', 'hod', 'cto',
    'super'
]
# Number of failed login attempts. When this number is exceeded,
# the user is prohibited from logging in for the specified ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT seconds.
# Set to None to disable this functionality.
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_SUBJECT_PREFIX = ' '


# Used by all-auth while generating links in email message.
# TODO: Not working. Check https://github.com/pennersr/django-allauth/issues/2318
DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = DEFAULT_HTTP_PROTOCOL
ACCOUNT_ADAPTER = 'authentication.adapters.CustomAccountAdapter'

#####################
# Admins
# Variables:
# ADMIN_EMAIL: All error reports will be sent to this email address
#####################
# TODO: Was sending too much HOST not allowed errors to the email specified. Re-enable after fixing the issue
# https://scanova.atlassian.net/browse/QCG-2076
ADMINS = [
    ('Admin', os.environ.get('ADMIN_EMAIL', 'admin@example.com'))
]
MANAGERS = ADMINS

#####################
# Email config
#####################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#####################
# Email Manager
#####################
"""
Default name to use along with DEFAULT_FROM_EMAIL while sending email
Ex: 'John Doe <john@example.com>'
"""
DEFAULT_FROM_EMAIL_NAME = os.environ.get('DEFAULT_FROM_EMAIL_NAME', 'Admin')

"""
Default email address to use to send the transactional emails from the application.
"""
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    '{} <{}>'.format(DEFAULT_FROM_EMAIL_NAME, 'support@example.com')
)

"""
Email address used to send server email (errors) by Django to the ADMIN and MANAGERS.
"""
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', DEFAULT_FROM_EMAIL)


#####################
# Debug Toolbar
#####################
"""
Used by Django-debug-toolbar. The toolbar will be displayed only on the listed IP addresses.
"""
INTERNAL_IPS = eval(os.environ.get('INTERNAL_IPS', "['127.0.0.1']"))
