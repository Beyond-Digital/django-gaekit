import os
from django.conf import global_settings

DEBUG = False,
USE_TZ = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}

CACHES = {
    "default": {
        "BACKEND": "gaekit.caches.GAEMemcachedCache"
    }
}
DEFAULT_FILE_STORAGE = 'gaekit.storages.CloudStorage'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}
PASSWORD_HASHERS = (
    # don't use the intentionally slow default password hasher
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
COMPRESS_ENABLED = False
WAGTAILSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'wagtail.wagtailsearch.backends.db.DBSearch',
    }
}
AUTH_USER_MODEL = 'tests.CustomUser'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    'taggit',
    'compressor',

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtaildocs',
    'wagtail.wagtailsnippets',
    'wagtail.wagtailusers',
    'wagtail.wagtailsites',
    'wagtail.wagtailimages',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsearch',
    'wagtail.wagtailforms',
    'wagtail.contrib.wagtailstyleguide',
    'wagtail.contrib.wagtailsitemaps',
    'wagtail.contrib.wagtailroutablepage',
    'wagtail.contrib.wagtailfrontendcache',
    'wagtail.tests',

    # Install wagtailredirects with its appconfig
    # Theres nothing special about wagtailredirects, we just need to have one
    # app which uses AppConfigs to test that hooks load properly
    'wagtail.wagtailredirects.apps.WagtailRedirectsAppConfig',
    "gaekit",
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
SITE_ID = 1
ROOT_URLCONF = 'tests.wagtail_urls'
WAGTAIL_SITE_NAME = "Test Site"

SECRET_KEY = 'not needed'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

WAGTAIL_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(WAGTAIL_ROOT, 'test-static')
