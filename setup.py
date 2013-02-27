#!/usr/bin/env python

from setuptools import setup
from uploadify import PROJECT, VERSION

setup(
    name=PROJECT,
    version=VERSION,
    description='Django integration of Uploadify jQuery plugin.',
    author='Dmitry Lazarko',
    author_email='alt0064@gmail.com',
    url='https://github.com/demetriuz/django-uploadify',
    packages=['uploadify', 'uploadify.templatetags'],
    package_data={'uploadify': ['templates/uploadify/*.html']},
    install_requires = [ 'django >= 1.3', 'django-misc' ],
)
