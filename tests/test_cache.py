# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from google.appengine.ext import testbed

from django.conf import settings
from django.core.cache import cache, get_cache
from django.middleware.cache import UpdateCacheMiddleware, FetchFromCacheMiddleware
from django.test import TestCase
from django.http import (HttpResponse, HttpRequest, QueryDict)

import random
import string
import time
import warnings

def custom_key_func(key, key_prefix, version):
    "A customized cache key function"
    return 'CUSTOM-' + '-'.join([key_prefix, str(version), key])

def expensive_calculation():
    expensive_calculation.num_runs += 1
    return timezone.now()

# functions/classes for complex data type tests
def f():
    return 42

class C:
    def m(n):
        return 24

class MemcachedCacheTests(TestCase):

    backend_name = 'gaekit.caches.GAEMemcachedCache'

    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_memcache_stub()
        self.cache = cache
        random_prefix = ''.join(random.choice(string.ascii_letters) for x in range(10))
        self.prefix_cache = get_cache(self.backend_name, KEY_PREFIX=random_prefix)
        self.v2_cache = cache
        self.custom_key_cache = get_cache(self.backend_name, KEY_FUNCTION=custom_key_func)
    
    def tearDown(self):
        self.cache.clear()

    def _get_request_cache(self, path):
        request = HttpRequest()
        request.META = {
            'SERVER_NAME': 'testserver',
            'SERVER_PORT': 80,
        }
        request.path = request.path_info = path
        request._cache_update_cache = True
        request.method = 'GET'
        return request

    def test_simple(self):
        # Simple cache set/get works
        self.cache.set("key", "value")
        self.assertEqual(self.cache.get("key"), "value")


    def test_add(self):
        # A key can be added to a cache
        self.cache.add("addkey1", "value")
        result = self.cache.add("addkey1", "newvalue")
        self.assertEqual(result, False)
        self.assertEqual(self.cache.get("addkey1"), "value")

    def test_prefix(self):
        # Test for same cache key conflicts between shared backend
        self.cache.set('somekey', 'value')

        # should not be set in the prefixed cache
        self.assertFalse(self.prefix_cache.has_key('somekey'))

        self.prefix_cache.set('somekey', 'value2')

        self.assertEqual(self.cache.get('somekey'), 'value')
        self.assertEqual(self.prefix_cache.get('somekey'), 'value2')




    def test_non_existent(self):
        # Non-existent cache keys return as None/default
        # get with non-existent keys
        self.assertEqual(self.cache.get("does_not_exist"), None)
        self.assertEqual(self.cache.get("does_not_exist", "bang!"), "bang!")

    def test_get_many(self):
        # Multiple cache keys can be returned using get_many
        self.cache.set('a', 'a')
        self.cache.set('b', 'b')
        self.cache.set('c', 'c')
        self.cache.set('d', 'd')
        self.assertEqual(self.cache.get_many(['a', 'c', 'd']), {'a' : 'a', 'c' : 'c', 'd' : 'd'})
        self.assertEqual(self.cache.get_many(['a', 'b', 'e']), {'a' : 'a', 'b' : 'b'})

    def test_delete(self):
        # Cache keys can be deleted
        self.cache.set("key1", "spam")
        self.cache.set("key2", "eggs")
        self.assertEqual(self.cache.get("key1"), "spam")
        self.cache.delete("key1")
        self.assertEqual(self.cache.get("key1"), None)
        self.assertEqual(self.cache.get("key2"), "eggs")

    def test_has_key(self):
        # The cache can be inspected for cache keys
        self.cache.set("hello1", "goodbye1")
        self.assertEqual(self.cache.has_key("hello1"), True)
        self.assertEqual(self.cache.has_key("goodbye1"), False)

    def test_in(self):
        # The in operator can be used to inspect cache contents
        self.cache.set("hello2", "goodbye2")
        self.assertEqual("hello2" in self.cache, True)
        self.assertEqual("goodbye2" in self.cache, False)

    def test_incr(self):
        # Cache values can be incremented
        self.cache.set('answer', 41)
        self.assertEqual(self.cache.incr('answer'), 42)
        self.assertEqual(self.cache.get('answer'), 42)
        self.assertEqual(self.cache.incr('answer', 10), 52)
        self.assertEqual(self.cache.get('answer'), 52)
        self.assertEqual(self.cache.incr('answer', -10), 42)
        self.assertRaises(ValueError, self.cache.incr, 'does_not_exist')

    def test_decr(self):
        # Cache values can be decremented
        self.cache.set('answer', 43)
        self.assertEqual(self.cache.decr('answer'), 42)
        self.assertEqual(self.cache.get('answer'), 42)
        self.assertEqual(self.cache.decr('answer', 10), 32)
        self.assertEqual(self.cache.get('answer'), 32)
        self.assertEqual(self.cache.decr('answer', -10), 42)
        self.assertRaises(ValueError, self.cache.decr, 'does_not_exist')

    def test_close(self):
        self.assertTrue(hasattr(self.cache, 'close'))
        self.cache.close()

    def test_data_types(self):
        # Many different data types can be cached
        stuff = {
            'string'    : 'this is a string',
            'int'       : 42,
            'list'      : [1, 2, 3, 4],
            'tuple'     : (1, 2, 3, 4),
            'dict'      : {'A': 1, 'B' : 2},
            'function'  : f,
            'class'     : C,
        }
        self.cache.set("stuff", stuff)
        self.assertEqual(self.cache.get("stuff"), stuff)

    def test_expiration(self):
        # Cache values can be set to expire
        self.cache.set('expire1', 'very quickly', 1)
        self.cache.set('expire2', 'very quickly', 1)
        self.cache.set('expire3', 'very quickly', 1)

        time.sleep(2)
        self.assertEqual(self.cache.get("expire1"), None)

        self.cache.add("expire2", "newvalue")
        self.assertEqual(self.cache.get("expire2"), "newvalue")
        self.assertEqual(self.cache.has_key("expire3"), False)

    def test_unicode(self):
        # Unicode values can be cached
        stuff = {
            'ascii': 'ascii_value',
            'unicode_ascii': 'Iñtërnâtiônàlizætiøn1',
            'Iñtërnâtiônàlizætiøn': 'Iñtërnâtiônàlizætiøn2',
            'ascii2': {'x' : 1 }
            }
        # Test `set`
        for (key, value) in stuff.items():
            self.cache.set(key, value)
            self.assertEqual(self.cache.get(key), value)

        # Test `add`
        for (key, value) in stuff.items():
            self.cache.delete(key)
            self.cache.add(key, value)
            self.assertEqual(self.cache.get(key), value)

        # Test `set_many`
        for (key, value) in stuff.items():
            self.cache.delete(key)
        self.cache.set_many(stuff)
        for (key, value) in stuff.items():
            self.assertEqual(self.cache.get(key), value)

    def test_binary_string(self):
        # Binary strings should be cacheable
        from zlib import compress, decompress
        value = 'value_to_be_compressed'
        compressed_value = compress(value.encode())

        # Test set
        self.cache.set('binary1', compressed_value)
        compressed_result = self.cache.get('binary1')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

        # Test add
        self.cache.add('binary1-add', compressed_value)
        compressed_result = self.cache.get('binary1-add')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

        # Test set_many
        self.cache.set_many({'binary1-set_many': compressed_value})
        compressed_result = self.cache.get('binary1-set_many')
        self.assertEqual(compressed_value, compressed_result)
        self.assertEqual(value, decompress(compressed_result).decode())

    def test_set_many(self):
        # Multiple keys can be set using set_many
        self.cache.set_many({"key1": "spam", "key2": "eggs"})
        self.assertEqual(self.cache.get("key1"), "spam")
        self.assertEqual(self.cache.get("key2"), "eggs")

    def test_set_many_expiration(self):
        # set_many takes a second ``timeout`` parameter
        self.cache.set_many({"key1": "spam", "key2": "eggs"}, 1)
        time.sleep(2)
        self.assertEqual(self.cache.get("key1"), None)
        self.assertEqual(self.cache.get("key2"), None)

    def test_delete_many(self):
        # Multiple keys can be deleted using delete_many
        self.cache.set("key1", "spam")
        self.cache.set("key2", "eggs")
        self.cache.set("key3", "ham")
        self.cache.delete_many(["key1", "key2"])
        self.assertEqual(self.cache.get("key1"), None)
        self.assertEqual(self.cache.get("key2"), None)
        self.assertEqual(self.cache.get("key3"), "ham")

    def test_clear(self):
        # The cache can be emptied using clear
        self.cache.set("key1", "spam")
        self.cache.set("key2", "eggs")
        self.cache.clear()
        self.assertEqual(self.cache.get("key1"), None)
        self.assertEqual(self.cache.get("key2"), None)

    def test_long_timeout(self):
        '''
        Using a timeout greater than 30 days makes memcached think
        it is an absolute expiration timestamp instead of a relative
        offset. Test that we honour this convention. Refs #12399.
        '''
        self.cache.set('key1', 'eggs', 60*60*24*30 + 1) #30 days + 1 second
        self.assertEqual(self.cache.get('key1'), 'eggs')

        self.cache.add('key2', 'ham', 60*60*24*30 + 1)
        self.assertEqual(self.cache.get('key2'), 'ham')

        self.cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, 60*60*24*30 + 1)
        self.assertEqual(self.cache.get('key3'), 'sausage')
        self.assertEqual(self.cache.get('key4'), 'lobster bisque')

    def test_forever_timeout(self):
        '''
        Passing in None into timeout results in a value that is cached forever
        '''
        self.cache.set('key1', 'eggs', None)
        self.assertEqual(self.cache.get('key1'), 'eggs')

        self.cache.add('key2', 'ham', None)
        self.assertEqual(self.cache.get('key2'), 'ham')

        self.cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, None)
        self.assertEqual(self.cache.get('key3'), 'sausage')
        self.assertEqual(self.cache.get('key4'), 'lobster bisque')

    def test_zero_timeout(self):
        '''
        Passing in None into timeout results in a value that is cached forever
        '''
        self.cache.set('key1', 'eggs', 0)
        self.assertEqual(self.cache.get('key1'), 'eggs')

        self.cache.add('key2', 'ham', 0)
        self.assertEqual(self.cache.get('key2'), 'ham')

        self.cache.set_many({'key3': 'sausage', 'key4': 'lobster bisque'}, 0)
        self.assertEqual(self.cache.get('key3'), 'sausage')
        self.assertEqual(self.cache.get('key4'), 'lobster bisque')

    def test_float_timeout(self):
        # Make sure a timeout given as a float doesn't crash anything.
        self.cache.set("key1", "spam", 100.2)
        self.assertEqual(self.cache.get("key1"), "spam")

    def test_cache_write_unpickable_object(self):
        update_middleware = UpdateCacheMiddleware()
        update_middleware.cache = self.cache

        fetch_middleware = FetchFromCacheMiddleware()
        fetch_middleware.cache = self.cache

        request = self._get_request_cache('/cache/test')
        get_cache_data = FetchFromCacheMiddleware().process_request(request)
        self.assertEqual(get_cache_data, None)

        response = HttpResponse()
        content = 'Testing cookie serialization.'
        response.content = content
        response.set_cookie('foo', 'bar')

        update_middleware.process_response(request, response)

        get_cache_data = fetch_middleware.process_request(request)
        self.assertNotEqual(get_cache_data, None)
        self.assertEqual(get_cache_data.content, content.encode('utf-8'))
        self.assertEqual(get_cache_data.cookies, response.cookies)

        update_middleware.process_response(request, get_cache_data)
        get_cache_data = fetch_middleware.process_request(request)
        self.assertNotEqual(get_cache_data, None)
        self.assertEqual(get_cache_data.content, content.encode('utf-8'))
        self.assertEqual(get_cache_data.cookies, response.cookies)