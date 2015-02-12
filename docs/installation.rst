============
Installation
============

To use with virtualenv, add the following to your requirements.txt::

    django-gaekit==0.2.9

As App Engine does not support installing requirements automatically,
you need to manually install dependencies to your project folder and
upload them with your app. One way to do this is with pip's --target
option::

    $ pip install -t libs -r requirements.txt

You then need to add the libs folder to your sys.path before libaries
are loaded. You can use appengine_config.py for this, since it's loaded
on startup in the SDK and on production environment::

    import sys
    sys.path.insert(0, 'path/to/lib')

You will also want to import this file (or copy the above) in your
manage.py, so libraries are loaded for runningmanagement commands::