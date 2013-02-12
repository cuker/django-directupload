.. image:: https://secure.travis-ci.org/cuker/django-directupload.png?branch=master
   :target: http://travis-ci.org/cuker/django-directupload

This is deprecated due to the difficulty of integrating reliably with the Django admin.

django-directupload is a Django application that offers direct uploading of files from your forms using jQuery-file-upload.

Requirements
============

* Python 2.6 or later
* Django 1.3 or later
* django-classy-tags


Installation
============

1) Ensure directupload is in your python path
2) Add the following line to your url patterns: ``(r'^directupload/', include('directupload.urls'))``
3) Add ``directupload`` to your INSTALLED_APPS
4) Insert the following into the head of your admin/change_form.html template: {% load directupload_tags %}{% directupload_head %}
5) Call directupload.admin.patch_admin to monkey patht the admin, this should be done before the admin.autodiscover is called


Installing S3 Support
=====================

To enable directuploads to your S3 bucket, set up the following in your settings::

    AWS_ACCESS_KEY_ID = 'accesskey'
    AWS_SECRET_ACCESS_KEY = 'secretkey'
    AWS_BUCKET_NAME = 'mybucket'
    UPLOADIFY_BACKEND = 'directupload.backends.s3.S3UploadifyBackend'


Features
========

* Utilizes jQuery-file-upload: http://blueimp.github.com/jQuery-File-Upload/
* Direct uploading backends, currently supports an internal django view or S3
* Admin integration via monkey patch or mixin
* Provides a widget class for integration with your django forms
* Prevents users from uploading over existing files using the desired name fetched from the storage backend

