#!/usr/bin/env python
# -*- codig: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='blackbird-chrony',
    version='0.1.0',
    description=(
        'get chrony information.'
    ),
    long_description=read('PROJECT.txt'),
    classifiers=[
      'Development Status :: 4 - Beta',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.6',
    ],
    author='makocchi',
    author_email='makocchi@gmail.com',
    url='https://github.com/Vagrants/blackbird-chrony',
    data_files=[
        ('/opt/blackbird/plugins', ['chrony.py']),
        ('/etc/blackbird/conf.d', ['chrony.cfg'])
    ],
    test_suite='tests',
)
