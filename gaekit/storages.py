# -*- coding: utf-8 -*-
from google.appengine.ext import blobstore
from google.appengine.api import images

from django.conf import settings
from django.core.files.storage import Storage

from gaekit.utils import cached

import mimetypes
import cloudstorage
import os
import datetime


class CloudStorage(Storage):

    def __init__(self, **kwargs):
        cloudstorage.validate_bucket_name(settings.GS_BUCKET_NAME)
        self.BUCKET_NAME = '/' + settings.GS_BUCKET_NAME

    def delete(self, filename):
        assert(filename)
        try:
            cloudstorage.delete(os.path.join(self.BUCKET_NAME, filename))
        except cloudstorage.NotFoundError:
            pass

    def exists(self, filename):
        try:
            cloudstorage.stat(os.path.join(self.BUCKET_NAME, filename))
            return True
        except cloudstorage.NotFoundError:
            return False

    def _open(self, filename, mode):
        return cloudstorage.open(os.path.join(self.BUCKET_NAME, filename), 'r')

    def _save(self, filename, content):
        with cloudstorage.open(os.path.join(self.BUCKET_NAME, filename),
            'w',
            content_type=mimetypes.guess_type(filename)[0],
            options={'x-goog-acl': 'public-read'}) as handle:
            handle.write(content.read())
        return os.path.join(self.BUCKET_NAME, filename)

    def created_time(self, filename):
        filestat = cloudstorage.stat(os.path.join(self.BUCKET_NAME, filename))
        return datetime.datetime.fromtimestamp(filestat.st_ctime)

    def path(self, name):
        return name

    def listdir(self, path):
        if path:
            realpath = os.path.join(self.BUCKET_NAME, path)
        else:
            realpath = self.BUCKET_NAME
        return ([], [obj.filename[len(self.BUCKET_NAME)+1:] for obj in cloudstorage.listbucket(realpath)])

    @cached
    def url(self, filename):
        key = blobstore.create_gs_key('/gs' + filename)
        return images.get_serving_url(key)