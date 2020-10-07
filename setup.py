#!/usr/bin/env python
# encoding: utf-8
import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (2, 7):
    sys.exit("requires python 2.7 and up")

here = os.path.dirname(__file__)

setup(name="rpyc_couchbase",
      version='0.0.1',
      description="Couchbase KV store implemented using RPyC",
      author="Tim Bradgate",
      author_email="tim.bradgate@couchbase.com",
      maintainer="Tim Bradgate",
      maintainer_email="tim.bradgate@couchbase.com",
      license="Copyright 2020 Couchbase",
      url="http://github.com/couchbaselabs",
      packages=[
          'rpyc_couchbase',
      ],
      tests_require=[],
      install_requires=["rpyc"],
      platforms=["POSIX", "Windows"],
      use_2to3=False,
      zip_safe=False,
      long_description=open(os.path.join(here, "README.md"), "r").read(),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: Other/Proprietary License',
          'Topic :: Database',
          'Topic :: Internet :: Log Analysis',
          'Programming Language :: Python :: 2',
      ],
      )