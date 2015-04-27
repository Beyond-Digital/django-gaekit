.. :changelog:

History
------

1.0.2 (2015-04-27)
++++++++++++++++++

* Adds wagtail.wagtailimages integration tests
* Storage.open now raises IOError if file doesn't exist
* Storage.size now raises OSError if file doesn't exist

1.0.1 (2015-03-24)
++++++++++++++++++

* Adds support for retrieving file size

1.0.0 (2015-02-18)
++++++++++++++++++

* Remove dependency on ImageService. URLs are now constructed from bucket name, with no RPC calls.
* Resolved inconsistencies with returning bucket name as part of path. This is now hidden.
* Deprecated ImageService-specific options. IMAGESERVICE_DEFAULT_SIZE and IMAGESERVICE_SECURE_URLS.
* Deprecated drf_extensions module.

0.2.9 (2014-08-13)
++++++++++++++++++

* Break out options IMAGESERVICE_DEFAULT_SIZE, IMAGESERVICE_SECURE_URLS and IMAGESERVICE_UPLOAD_HEADERS

0.2.8 (2014-08-13)
++++++++++++++++++

* Duff release

0.2.7 (2014-04-17)
++++++++++++++++++

* Add FeedListKeyConstructor for drf_extensions

0.1.4 (2014-03-10)
++++++++++++++++++

* Add fallback for cloud storage urls

0.1.3 (2014-03-10)
++++++++++++++++++

* Add exception logging if URL generation fails

0.1.2 (2014-03-07)
++++++++++++++++++

* Remove utils (lock, memoizer)
* Monkeypatch ReadBuffer to add open() stub (fixes issue with easy_thumbnails)

0.1.1 (2013-10-10)
++++++++++++++++++

* Fix for distributed lock

0.1.0 (2013-08-15)
++++++++++++++++++

* First release on PyPI.