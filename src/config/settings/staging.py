from .base import *

ALLOWED_HOSTS += [
    "greenaralsea.org",
    "localhost",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DJANGO_DB_NAME', 'db'),
        'USER': os.environ.get('DJANGO_DB_USER', 'atabek'),
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

# DEBUG = os.environ.get('DJANGO_DEBUG') or False
DEBUG = True

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

# -----------------------------------------------------------------------------
# MUST BE DELETED IN PRODUCTION 
# -----------------------------------------------------------------------------

BASE_APPS = [
    'jazzmin',
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
    'axes',
]

LOCAL_APPS = [
    'api',
]

INSTALLED_APPS = BASE_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'axes.middleware.AxesMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

JAZZMIN_SETTINGS = {
    "site_title": "GreenAralSea.org Portal",
    "site_header": "GreenAralSea.org Admin",
#    "site_logo": "logo.jpeg",
    "login_logo": None,
    "welcome_sign": "Welcome to Aral Sea website admin panel",
    "copyright": "AralTech Ltd",
        "usermenu_links": [
        {"name": "Contact to developer", "url": "https://t.me/AralTech_Dev", "new_window": True},
        {"model": "auth.user"}
    ],

    "show_title": True,
    "show_sidebar": True,
    "navigation_expanded": False,
    "search_bar": True,
    "show_ui_builder": True,
}

AUTHENTICATION_BACKENDS = [
    # Django default auth backends
    'django.contrib.auth.backends.ModelBackend',

    # AxesBackend should be the last backend in the AUTHENTICATION_BACKENDS list
    'axes.backends.AxesBackend',
]