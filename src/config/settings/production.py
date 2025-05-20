from .base import *

ALLOWED_HOSTS += [
    "greenaralsea.org",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'db'),
        'USER': os.environ.get('DJANGO_DB_USER', 'user'),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', 'qwe123'),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DB_PORT', 5432),
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),
]

STATIC_URL = '/django/static/'
STATIC_ROOT = os.environ.get(
    'DJANGO_STATIC_ROOT',
    os.path.join(BASE_DIR, 'static')
)

DEBUG = False

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'sjhn3id*9m-8lo6a-3jktg3@uewdjx1q(yatlzo^*a5e=qjmyb'
)

MEDIA_ROOT = os.environ.get(
    'DJANGO_MEDIA_ROOT',
    os.path.join(BASE_DIR, 'media')
)
MEDIA_URL = '/media/'

PAYSYS_VENDOR_ID = os.environ.get(
    'DJANGO_PAYSYS_VENDOR_ID',
    '100821'
)
PAYSYS_SECRET_KEY = os.environ.get(
    'DJANGO_PAYSYS_SECRET_KEY',
    'N#SS*6IfHkW@yW0V34uLz6DmVDkqPfF1',
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
