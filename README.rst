=============================
django-gaekit
=============================
    
.. image:: https://travis-ci.org/Beyond-Digital/django-gaekit.png?branch=master
        :target: https://travis-ci.org/Beyond-Digital/django-gaekit

.. image:: https://pypip.in/version/django-gaekit/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/django-gaekit/
    :alt: Latest Version

.. image:: https://requires.io/github/Beyond-Digital/django-gaekit/requirements.svg?branch=master
     :target: https://requires.io/github/Beyond-Digital/django-gaekit/requirements/?branch=master
     :alt: Requirements Status

Collection of backends, wrappers and utilities to enquicken django development on Google App Engine

Documentation
-------------

The full documentation is at http://django-gaekit.rtfd.org.

Quickstart
----------

Use template from https://github.com/Beyond-Digital/bynd-django-gae

To use with virtualenv, add the following to your requirements.txt::

    django-gaekit==0.2.9

To use the storage backend, add the following to your settings module::

    DEFAULT_FILE_STORAGE = 'gaekit.storages.CloudStorage'
    GS_BUCKET_NAME = 'bucket_name'

To use the cache backend, add the following to your settings module::

    CACHES = {
        'default': {
            'BACKEND': 'gaekit.caches.GAEMemcachedCache',
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
