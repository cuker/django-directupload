#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

version = '0.0.1'

setup(name='django-directupload',
      version=version,
      description='A Django application that offers direct uploading of files from your forms using Uploadify.',
      author='Jason Kraus',
      author_email='jasonk@cukerinteractive.com',
      url='https://github.com/cuker/django-directupload',
      packages=find_packages(exclude=['test_environment']),
      include_package_data = True,
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
      )

