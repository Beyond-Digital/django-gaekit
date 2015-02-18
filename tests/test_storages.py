# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import errno
import os
import shutil
import sys
import tempfile
import time
import unittest
import zlib
from datetime import datetime, timedelta
from io import BytesIO

try:
    import threading
except ImportError:
    import dummy_threading as threading

from django.conf import settings
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured
from django.core.files.base import File, ContentFile
from django.core.files.images import get_image_dimensions
from django.core.files.storage import FileSystemStorage, get_storage_class
from django.core.files.uploadedfile import UploadedFile
from django.test import LiveServerTestCase, SimpleTestCase
from django.test.utils import override_settings
from django.utils import six
# from django.utils.six.moves.urllib.request import urlopen
from django.utils._os import upath
from gaekit.storages import CloudStorage
from google.appengine.ext import testbed

try:
    from django.utils.image import Image
except ImportError, ImproperlyConfigured:
    Image = None


class BlobStorageTests(unittest.TestCase):
    storage_class = CloudStorage

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_all_stubs()
        self.storage = self.storage_class()

    def test_exists(self):
        self.assertFalse(self.storage.exists('test.file'))
        f = ContentFile('custom contents')
        storage_f_name = self.storage.save('test.file', f)
        print(storage_f_name)
        self.assertTrue(self.storage.exists(storage_f_name))

    def test_file_created_time(self):
        """
        File storage returns a Datetime object for the creation time of
        a file.
        """
        self.assertFalse(self.storage.exists('test.file'))

        f = ContentFile('custom contents')
        f_name = self.storage.save('test.file', f)
        ctime = self.storage.created_time(f_name)

        self.assertTrue(datetime.now() - self.storage.created_time(f_name) < timedelta(seconds=2))

        self.storage.delete(f_name)

    def test_file_save_without_name(self):
        """
        File storage extracts the filename from the content object if no
        name is given explicitly.
        """
        self.assertFalse(self.storage.exists('test.file'))

        f = ContentFile('custom contents')
        f.name = 'test.file'
        storage_f_name = self.storage.save(None, f)
        self.assertTrue(self.storage.exists(f.name))
        self.storage.delete(storage_f_name)

    def test_save_file_contents(self):
        self.assertFalse(self.storage.exists('test.file'))
        f = ContentFile('custom contents')
        storage_f_name = self.storage.save('test.file', f)

        with self.storage.open('test.file', 'r') as contents:
            self.assertEqual(contents.read(), 'custom contents')

    def test_file_get_url(self):
        self.assertFalse(self.storage.exists('test.file'))
        f = ContentFile('custom contents')
        storage_f_name = self.storage.save('test.file', f)
        self.assertTrue(self.storage.url(storage_f_name))

    def test_file_path(self):
        """
        File storage returns the full path of a file
        """
        self.assertFalse(self.storage.exists('test.file'))

        f = ContentFile('custom contents')
        f_name = self.storage.save('test.file', f)

        self.assertEqual(self.storage.path(f_name), f_name)

        self.storage.delete(f_name)

    def test_file_storage_preserves_filename_case(self):
        """The storage backend should preserve case of filenames."""
        # Create a storage backend associated with the mixed case name
        # directory.

        # Ask that storage backend to store a file with a mixed case filename.
        mixed_case = 'CaSe_SeNsItIvE'
        self.assertFalse(self.storage.exists(mixed_case))
        f = ContentFile('custom contents')
        f_name = self.storage.save(mixed_case, f)
        self.assertTrue(mixed_case in f_name)
        self.storage.delete(f_name)

    def test_delete_no_name(self):
        """
        Calling delete with an empty name should not try to remove the base
        storage directory, but fail loudly (#20660).
        """
        with self.assertRaises(AssertionError):
            self.storage.delete('')
