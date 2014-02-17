#!/usr/bin/env python

import os

try:
    from setuptools import setup, Extension, Command
except ImportError:
    from distutils.core import setup, Extension, Command

import hashify

dependencies = ['path.py']

setup(
    name=hashify.__name__,
    version=hashify.__version__,
    description=hashify.__description__,
    long_description=open('README.rst').read(),
    author=hashify.__author__,
    author_email=hashify.__author_email__,
    url=hashify.__url__,
    license=hashify.__license__,
    packages=['hashify'],
    #test_suite='tests',
    install_requires=dependencies,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: System',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: System :: Filesystems',
    ],
    entry_points={
        'console_scripts': [
            'hashify = hashify.__main__:main',
        ],
    }
)
