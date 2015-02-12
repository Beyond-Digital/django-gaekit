================
Configuration
================

``IMAGESERVICE_DEFAULT_SIZE`` will be passed to the AppEngine get_serving_url
function. From the documentation:

   "An integer supplying the size of resulting images. When resizing or cropping an image, you must specify the new size using an integer 0 to 1600. The maximum size is defined in IMG_SERVING_SIZES_LIMIT. The API resizes the image to the supplied value, applying the specified size to the image's longest dimension and preserving the original aspect ratio. A size of 0 returns the original image."

``IMAGESERVICE_SECURE_URLS`` sets the secure_url param on get_serving_url.
Default is True, so you only need to set this if you wish to have non-https links. 
Note that the SDK will not generate secure URLs under any circumstances.

``IMAGESERVICE_UPLOAD_HEADERS`` sets the headers that are set when the file is
uploaded to cloud storage. This defaults to "{'x-goog-acl': 'public-read'}", which
will make your files world-readable. 