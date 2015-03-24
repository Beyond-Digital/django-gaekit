# -*- coding: utf-8 -*-
from google.appengine.ext import blobstore
from google.appengine.api import images

from django.conf import settings
from django.core.files.storage import Storage

import mimetypes
import cloudstorage
import datetime

from .utils import is_hosted

HEADERS = {'x-goog-acl': 'public-read'}
if hasattr(settings, 'IMAGESERVICE_UPLOAD_HEADERS'):
    HEADERS = getattr(settings, 'IMAGESERVICE_UPLOAD_HEADERS')


class CloudStorage(Storage):

    def __init__(self, **kwargs):
        cloudstorage.validate_bucket_name(settings.GS_BUCKET_NAME)
        self.bucket_name = settings.GS_BUCKET_NAME

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
        stats = cloudstorage.stat(self._real_path(name))
        return stats.st_size

    def _open(self, filename, mode):
        readbuffer = cloudstorage.open(self._real_path(filename), 'r')
        readbuffer.open = lambda x: True
        return readbuffer

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
