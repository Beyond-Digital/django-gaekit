import os
from django.conf import global_settings

DEBUG=False,
USE_TZ=True
DATABASES={
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    }
}
CACHES={
    "default": {
        "BACKEND": "gaekit.caches.GAEMemcachedCache"
    }
}
DEFAULT_FILE_STORAGE='gaekit.storages.CloudStorage'

INSTALLED_APPS=[
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
    'wagtail.wagtailusers',
    'wagtail.wagtailimages',
    'wagtail.wagtailredirects.apps.WagtailRedirectsAppConfig',

    "gaekit",
]
MIDDLEWARE_CLASSES=(
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)
SITE_ID=1
ROOT_URLCONF='tests.wagtail_urls'
WAGTAIL_SITE_NAME="Test Site"

SECRET_KEY = 'not needed'
STATIC_URL = '/static/'

WAGTAIL_ROOT = os.path.dirname(__file__)
STATIC_ROOT = os.path.join(WAGTAIL_ROOT, 'test-static')
