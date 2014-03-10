# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys

import gaekit

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = gaekit.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-gaekit',
    version=version,
    description='Collection of backends, wrappers and utilities to enquicken django development on Google App Engine',
    long_description=readme + '\n\n' + history,
    author='George Whewell',
    author_email='george@bynd.com',
    url='https://github.com/Beyond-Digital/django-gaekit',
    packages=[
        'gaekit',
    ],
    include_package_data=True,
    install_requires=[
        'GoogleAppEngineCloudStorageClient==1.8.3.1'
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-gaekit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
