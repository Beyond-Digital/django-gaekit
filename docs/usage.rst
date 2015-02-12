========
Usage
========

Storage Backend
-----------------

To use the storage backend, add the following to your settings module::

    DEFAULT_FILE_STORAGE = 'gaekit.storages.CloudStorage'
    GS_BUCKET_NAME = 'your_project_name'


Cache
------

To use the cache backend, add the following to your settings module::

    CACHES = {
        'default': {
            'BACKEND': 'gaekit.caches.GAEMemcachedCache',
        }
    }

Blacklist
-----------

To import blacklisted modules, in your **local** settings module::
    
    from gaekit.boot import break_sandbox
    break_sandbox()
