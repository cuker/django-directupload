django-directupload is a Django application that offers direct uploading of files from your forms using Uploadify.

Requirements
============

* Django 1.3 or later
* django-classy-tags


Installation
============

# Ensure directupload is in your python path
# Add the following line to your url patterns: ``(r'^uploadify/', include('directupload.urls'))``
# Add ``directupload`` to your INSTALLED_APPS
# Insert the following into the head of your admin/change_form.html template: {% load uploadify_tags %}{% uploadify_head %}


Features
========

* Utilizes Uploadify 3.0 (beta)
* Direct uploading backends, currently supports an internal django view or S3
* Admin integration via monkey patch or mixin
* Provides a widget class for integration with your django forms
* Prevents users from uploading over existing files using the desired name fetched from the storage backend

