#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from io import open
import os
import setuptools
import sys


# Delete os.link if we are using Vagrant, because tox requires a file
# system with hard links to work.
#
# The hard link only saves a little disk space, so you should not care
if os.environ.get('USER','') == 'vagrant':
    try:
        del os.link
    except AttributeError:
        pass


BASE_DIR = os.path.dirname(__file__)
PKG_DIR = os.path.join(BASE_DIR, "cpe")

meta = {}
with open(os.path.join(PKG_DIR, "__meta__.py"), 'rb') as f:
    exec(f.read(), meta)

with open(os.path.join(BASE_DIR, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

install_requires = []

if sys.version_info[:2] < (2, 7):
    install_requires.append('ordereddict')


setuptools.setup(
    name=meta["__packagename__"],
    version=meta["__version__"],
    description=meta["__summary__"],
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7"
    ],
    keywords=meta["__keywords__"],
    author=meta["__author__"],
    author_email=meta["__email__"],
    maintainer=meta["__maintainer__"],
    maintainer_email=meta["__maintainer_email__"],
    license=meta["__license__"],
    url=meta["__url__"],
    include_package_data=False,
    install_requires=install_requires,
    packages=(b'cpe', b'cpe.comp'),
)
