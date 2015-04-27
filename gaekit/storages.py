# -*- coding: utf-8 -*-
from google.appengine.ext import blobstore
from google.appengine.api import images
from google.appengine.api import app_identity

from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import ContentFile

import mimetypes
import cloudstorage
import datetime

from .utils import is_hosted

HEADERS = {'x-goog-acl': 'public-read'}
if hasattr(settings, 'IMAGESERVICE_UPLOAD_HEADERS'):
    HEADERS = getattr(settings, 'IMAGESERVICE_UPLOAD_HEADERS')


class CloudStorage(Storage):

    def __init__(self, **kwargs):
        self.bucket_name = getattr(settings, 'GS_BUCKET_NAME', None)
        if self.bucket_name is None:
            self.bucket_name = app_identity.get_default_gcs_bucket_name()
        cloudstorage.validate_bucket_name(self.bucket_name)

    def _real_path(self, path):
        return '/' + self.bucket_name + '/' + path

    def _fake_path(self, path):
        return path[len(self._real_path('')):]

    def delete(self, filename):
        assert(filename)
        try:
            cloudstorage.delete(self._real_path(filename))
        except cloudstorage.NotFoundError:
            pass

    def exists(self, filename):
        try:
            cloudstorage.stat(self._real_path(filename))
            return True
        except cloudstorage.NotFoundError:
            return False

    def size(self, name):
        try:
            stats = cloudstorage.stat(self._real_path(name))
            return stats.st_size
        except cloudstorage.NotFoundError as exp:
            raise OSError(str(exp))

    def _open(self, filename, mode):
        try:
            readbuffer = cloudstorage.open(self._real_path(filename), 'r')
            return ContentFile(readbuffer.read(), name=filename)
        except cloudstorage.NotFoundError as exp:
            raise IOError(str(exp))

    def _save(self, filename, content):
        with cloudstorage.open(
            self._real_path(filename), 'w',
            content_type=mimetypes.guess_type(filename)[0],
            options=HEADERS
        ) as handle:
            handle.write(content.read())
        return filename

    def created_time(self, filename):
        filestat = cloudstorage.stat(self._real_path(filename))
        return datetime.datetime.fromtimestamp(filestat.st_ctime)

    def path(self, name):
        return name

    def url(self, filename):
        if not is_hosted():
            key = blobstore.create_gs_key('/gs' + self._real_path(filename))
            return images.get_serving_url(key)
        return 'https://storage.googleapis.com{path}'.format(
            path=self._real_path(filename)
        )
