=============================
django-gaekit
=============================

.. image:: https://badge.fury.io/py/django-gaekit.png
    :target: http://badge.fury.io/py/django-gaekit
    
.. image:: https://travis-ci.org/georgewhewell/django-gaekit.png?branch=master
        :target: https://travis-ci.org/Beyond-Digital/django-gaekit

.. image:: https://pypip.in/d/django-gaekit/badge.png
        :target: https://crate.io/packages/django-gaekit?version=latest


Collection of backends, wrappers and utilities to enquicken django development on Google App Engine

Documentation
-------------

The full documentation is at http://django-gaekit.rtfd.org.

Quickstart
----------

Use template from https://github.com/Beyond-Digital/bynd-django-gae

To use with virtualenv, add the following to your requirements.txt::

    django-gaekit==0.1.4

To use the storage backend, add the following to your settings module::

    DEFAULT_FILE_STORAGE = 'gaekit.storages.CloudStorage'
    GS_BUCKET_NAME = 'bucket_name'

To use the cache backend, add the following to your settings module::

    CACHES = {
        'default': {
            'BACKEND': 'gaekit.caches.GAEMemcachedCache',
            'TIMEOUT': 0,
        }
    }

To import blacklisted modules, in your **local** settings module::
    
    from gaekit.boot import break_sandbox
    break_sandbox()

Features
--------

* Storage Backend using Google Cloud Storage
* Cache backend using Memcache
* Import blacklisted modules in the SDK (eg sqlite3)

