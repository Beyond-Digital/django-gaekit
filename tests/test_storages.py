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

    # def tearDown(self):
    #     shutil.rmtree(self.temp_dir)
    #     shutil.rmtree(self.temp_dir2)

    def test_exists(self):
        self.assertFalse(self.storage.exists('test.file'))
        f = ContentFile('custom contents')
        storage_f_name = self.storage.save('test.file', f)
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
        self.assertEqual(storage_f_name, '/' + settings.GS_BUCKET_NAME + '/' + f.name)
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

        self.assertEqual(self.storage.path(f_name),
            os.path.join('/' + settings.GS_BUCKET_NAME, f_name))

        self.storage.delete(f_name)

    def test_listdir(self):
        """
        File storage returns a tuple containing directories and files.
        """
        self.assertFalse(self.storage.exists('storage_test_1'))
        self.assertFalse(self.storage.exists('storage_test_2'))
        self.assertFalse(self.storage.exists('storage_dir_1'))

        f = self.storage.save('storage_test_1', ContentFile('custom content'))
        f = self.storage.save('storage_test_2', ContentFile('custom content'))
        # os.mkdir(os.path.join(self.temp_dir, 'storage_dir_1'))

        dirs, files = self.storage.listdir('')
        self.assertEqual(set(files),
                         set(['storage_test_1', 'storage_test_2']))

        self.storage.delete('storage_test_1')
        self.storage.delete('storage_test_2')

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


# class FileStoragePathParsing(unittest.TestCase):
#     def setUp(self):
#         self.storage_dir = tempfile.mkdtemp()
#         self.storage = FileSystemStorage(self.storage_dir)

#     def tearDown(self):
#         shutil.rmtree(self.storage_dir)

#     def test_directory_with_dot(self):
#         """Regression test for #9610.

#         If the directory name contains a dot and the file name doesn't, make
#         sure we still mangle the file name instead of the directory name.
#         """

#         self.storage.save('dotted.path/test', ContentFile("1"))
#         self.storage.save('dotted.path/test', ContentFile("2"))

#         self.assertFalse(os.path.exists(os.path.join(self.storage_dir, 'dotted_.path')))
#         self.assertTrue(os.path.exists(os.path.join(self.storage_dir, 'dotted.path/test')))
#         self.assertTrue(os.path.exists(os.path.join(self.storage_dir, 'dotted.path/test_1')))

#     def test_first_character_dot(self):
#         """
#         File names with a dot as their first character don't have an extension,
#         and the underscore should get added to the end.
#         """
#         self.storage.save('dotted.path/.test', ContentFile("1"))
#         self.storage.save('dotted.path/.test', ContentFile("2"))

#         self.assertTrue(os.path.exists(os.path.join(self.storage_dir, 'dotted.path/.test')))
#         self.assertTrue(os.path.exists(os.path.join(self.storage_dir, 'dotted.path/.test_1')))

# class DimensionClosingBug(unittest.TestCase):
#     """
#     Test that get_image_dimensions() properly closes files (#8817)
#     """
#     @unittest.skipUnless(Image, "Pillow/PIL not installed")
#     def test_not_closing_of_files(self):
#         """
#         Open files passed into get_image_dimensions() should stay opened.
#         """
#         empty_io = BytesIO()
#         try:
#             get_image_dimensions(empty_io)
#         finally:
#             self.assertTrue(not empty_io.closed)

#     @unittest.skipUnless(Image, "Pillow/PIL not installed")
#     def test_closing_of_filenames(self):
#         """
#         get_image_dimensions() called with a filename should closed the file.
#         """
#         # We need to inject a modified open() builtin into the images module
#         # that checks if the file was closed properly if the function is
#         # called with a filename instead of an file object.
#         # get_image_dimensions will call our catching_open instead of the
#         # regular builtin one.

#         class FileWrapper(object):
#             _closed = []
#             def __init__(self, f):
#                 self.f = f
#             def __getattr__(self, name):
#                 return getattr(self.f, name)
#             def close(self):
#                 self._closed.append(True)
#                 self.f.close()

#         def catching_open(*args):
#             return FileWrapper(open(*args))

#         from django.core.files import images
#         images.open = catching_open
#         try:
#             get_image_dimensions(os.path.join(os.path.dirname(upath(__file__)), "test1.png"))
#         finally:
#             del images.open
#         self.assertTrue(FileWrapper._closed)

# class InconsistentGetImageDimensionsBug(unittest.TestCase):
#     """
#     Test that get_image_dimensions() works properly after various calls
#     using a file handler (#11158)
#     """
#     @unittest.skipUnless(Image, "Pillow/PIL not installed")
#     def test_multiple_calls(self):
#         """
#         Multiple calls of get_image_dimensions() should return the same size.
#         """
#         from django.core.files.images import ImageFile

#         img_path = os.path.join(os.path.dirname(upath(__file__)), "test.png")
#         with open(img_path, 'rb') as file:
#             image = ImageFile(file)
#             image_pil = Image.open(img_path)
#             size_1, size_2 = get_image_dimensions(image), get_image_dimensions(image)
#         self.assertEqual(image_pil.size, size_1)
#         self.assertEqual(size_1, size_2)

#     @unittest.skipUnless(Image, "Pillow/PIL not installed")
#     def test_bug_19457(self):
#         """
#         Regression test for #19457
#         get_image_dimensions fails on some pngs, while Image.size is working good on them
#         """
#         img_path = os.path.join(os.path.dirname(upath(__file__)), "magic.png")
#         try:
#             size = get_image_dimensions(img_path)
#         except zlib.error:
#             self.fail("Exception raised from get_image_dimensions().")
#         self.assertEqual(size, Image.open(img_path).size)


# class ContentFileTestCase(unittest.TestCase):

#     def setUp(self):
#         self.storage_dir = tempfile.mkdtemp()
#         self.storage = FileSystemStorage(self.storage_dir)

#     def tearDown(self):
#         shutil.rmtree(self.storage_dir)

#     def test_content_file_default_name(self):
#         self.assertEqual(ContentFile(b"content").name, None)

#     def test_content_file_custom_name(self):
#         """
#         Test that the constructor of ContentFile accepts 'name' (#16590).
#         """
#         name = "I can have a name too!"
#         self.assertEqual(ContentFile(b"content", name=name).name, name)

#     def test_content_file_input_type(self):
#         """
#         Test that ContentFile can accept both bytes and unicode and that the
#         retrieved content is of the same type.
#         """
#         self.assertIsInstance(ContentFile(b"content").read(), bytes)
#         if six.PY3:
#             self.assertIsInstance(ContentFile("español").read(), six.text_type)
#         else:
#             self.assertIsInstance(ContentFile("español").read(), bytes)

#     def test_content_saving(self):
#         """
#         Test that ContentFile can be saved correctly with the filesystem storage,
#         both if it was initialized with string or unicode content"""
#         self.storage.save('bytes.txt', ContentFile(b"content"))
#         self.storage.save('unicode.txt', ContentFile("español"))


# class NoNameFileTestCase(unittest.TestCase):
#     """
#     Other examples of unnamed files may be tempfile.SpooledTemporaryFile or
#     urllib.urlopen()
#     """
#     def test_noname_file_default_name(self):
#         self.assertEqual(File(BytesIO(b'A file with no name')).name, None)

#     def test_noname_file_get_size(self):
#         self.assertEqual(File(BytesIO(b'A file with no name')).size, 19)


# class FileLikeObjectTestCase(LiveServerTestCase):
#     """
#     Test file-like objects (#15644).
#     """

#     available_apps = []
#     urls = 'file_storage.urls'

#     def setUp(self):
#         self.temp_dir = tempfile.mkdtemp()
#         self.storage = FileSystemStorage(location=self.temp_dir)

#     def tearDown(self):
#         shutil.rmtree(self.temp_dir)

#     def test_urllib2_urlopen(self):
#         """
#         Test the File storage API with a file like object coming from urllib2.urlopen()
#         """
#         file_like_object = urlopen(self.live_server_url + '/')
#         f = File(file_like_object)
#         stored_filename = self.storage.save("remote_file.html", f)

#         remote_file = urlopen(self.live_server_url + '/')
#         with self.storage.open(stored_filename) as stored_file:
#             self.assertEqual(stored_file.read(), remote_file.read())