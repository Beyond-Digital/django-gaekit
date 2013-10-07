from django.core.cache import cache
from functools import wraps

import copy
import time
import logging
import contextlib
import random
 

class MemcacheLockException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
 
@contextlib.contextmanager
def memcache_lock(key, attempts=1, expires=30):
    key = '__d_lock_%s' % key
 
    got_lock = False
    try:
        got_lock = _acquire_lock(key, attempts, expires)
        yield
    finally:
        if got_lock:
            _release_lock(key)
 
def _acquire_lock(key, attempts, expires):
    for i in xrange(0, attempts):
        stored = cache.add(key, 1, expires)
        if stored:
            return True
        if i != attempts-1:
            sleep_time = (((i+1)*random.random()) + 2**i) / 2.5
            logging.debug('Sleeping for %s while trying to acquire key %s', sleep_time, key)
            time.sleep(sleep_time)
    raise MemcacheLockException('Could not acquire lock for %s' % key)
 
def _release_lock(key):
    cache.delete(key)

def distlock(func, attempts=1, expires=30):
    def locked_func(*args):
        try:
            with memcache_lock([func.__name__] + args, attempts, expires):
                return func(args)
        except MemcacheLockException: 
            return False

    return locked_func

def make_hash(obj):
    """Make a hash from an arbitrary nested dictionary, list, tuple or
    set.

    """
    if isinstance(obj, set) or isinstance(obj, tuple) or isinstance(obj, list):
        return hash(tuple([make_hash(e) for e in obj]))

    elif not isinstance(obj, dict):
        return hash(obj)

    new_obj = copy.deepcopy(obj)
    for k, v in new_obj.items():
        new_obj[k] = make_hash(v)

    return hash(tuple(frozenset(new_obj.items())))

def cached(function, seconds=0):
    """Return a version of this function that caches its results for
    the time specified.

    >>> def foo(x): print "called"; return 1
    >>> cached(foo)('whatever')
    called
    1
    >>> cached(foo)('whatever')
    1

    """
    @wraps(function)
    def get_cache_or_call(*args, **kwargs):
        # known bug: if the function returns None, we never save it in
        # the cache
        cache_key = make_hash((function.__module__ + function.__name__, 
                              args, kwargs))

        cached_result = cache.get(cache_key)
        if cached_result is None:
            result = function(*args)
            cache.set(cache_key, result, seconds)
            return result
        else:
            return cached_result

    return get_cache_or_call
