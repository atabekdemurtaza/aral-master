from .base import *

ALLOWED_HOSTS += [
    "127.0.0.1",
    "192.168.1.134",
]

# Application definition

# -----------------------------------------------------------------------------
# Section related to CORS configuration
# -----------------------------------------------------------------------------

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
    'tinymce',
]

LOCAL_APPS = [
    'api',
]

INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# -----------------------------------------------------------------------------
# End of CORS configuration
# -----------------------------------------------------------------------------


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
# Overriding database parameter 

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME': os.environ.get('DB_NAME', 'aral'),
	'USER': os.environ.get('DB_USER', 'aral'),
        'HOST': 'localhost'
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/django/static/'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sjhn3id*9m-8lo6a-3jktg3@uewdjx1q(yatlzo^*a5e=qjmyb'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

PAYSYS_VENDOR_ID = '100821'
PAYSYS_SECRET_KEY = 'N#SS*6IfHkW@yW0V34uLz6DmVDkqPfF1'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
