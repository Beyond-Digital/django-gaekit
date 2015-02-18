================
Configuration
================

``IMAGESERVICE_UPLOAD_HEADERS`` sets the headers that are set when the file is
uploaded to cloud storage. This defaults to "{'x-goog-acl': 'public-read'}", which
will make your files world-readable. 