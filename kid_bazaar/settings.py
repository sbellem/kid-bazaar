"""
Django settings for kid_bazaar project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@j&z6137cg)^h#tzgas%8sh(+xwx1hjl2=$5wu)c8msi*-g=$0'

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

    'bootstrap3',
    'cloudinary',
    'custom_user',
    'south',
    'cloudinary',
    'paypal.standard.ipn',

    'kid_bazaar.apps.payments',
    'kid_bazaar.apps.home',

)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'kid_bazaar.libs.passwordless_backend.PasswordlessAuthBackend',
)

AUTH_USER_MODEL = 'home.KBUser'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth',
)


ROOT_URLCONF = 'kid_bazaar.urls'

WSGI_APPLICATION = 'kid_bazaar.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


## HEROKU/CLOUDCONTROL SETTINGS ##

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)


PAYPAL_RECEIVER_EMAIL = "mat.jankowski+sandbox@gmail.com"
#PAYPAL_TEST = True

## KID-BAZAAR SETINGS ##

BRAINTREE_MERCHANT_ACCOUNT_ID = 'rzm4w7q6cyjy97z3'
BRAINTREE_MERCHANT_ID = '9tr9c2z2g3brts8d'
BRAINTREE_PUBLIC_KEY = '42shpdp9smzw6z4w'
BRAINTREE_PRIVATE_KEY = '2472860acb14f14150a7f523bd489895'

# sendgrid email sending
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'app26556402@heroku.com'
EMAIL_HOST_PASSWORD = 'gf0dr6zq'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

HOST = os.environ.get('HOST', 'https://kidsbazaar.cloudcontrolapp.com')
