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
    "tests",
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
SITE_ID=1
ROOT_URLCONF='tests.wagtail_urls'
WAGTAIL_SITE_NAME="Test Site"
SECRET_KEY = 'notasecret'