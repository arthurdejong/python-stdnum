#!/usr/bin/env python

# setup.py - python-stdnum installation script
#
# Copyright (C) 2010-2021 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""python-stdnum installation script."""

import os
import sys

from setuptools import find_packages, setup

import stdnum


# fix permissions for sdist
if 'sdist' in sys.argv:
    os.system('chmod -R a+rX .')
    os.umask(int('022', 8))

base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, 'README'), 'rb') as fp:
    long_description = fp.read().decode('utf-8')

setup(
    name='python-stdnum',
    version=stdnum.__version__,
    description='Python module to handle standardized numbers and codes',
    long_description=long_description,
    author='Arthur de Jong',
    author_email='arthur@arthurdejong.org',
    url='https://arthurdejong.org/python-stdnum/',
    project_urls={
        'Documentation': 'https://arthurdejong.org/python-stdnum/doc/',
        'GitHub': 'https://github.com/arthurdejong/python-stdnum/',
    },
    license='LGPL',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business :: Financial',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: General',
    ],
    packages=find_packages(),
    install_requires=[],
    package_data={'': ['*.dat']},
    extras_require={
        # The SOAP feature is only required for a number of online tests
        # of numbers such as the EU VAT VIES lookup, the Dominican Republic
        # DGII services or the Turkish T.C. Kimlik validation.
        'SOAP': ['zeep'],      # recommended implementation
        'SOAP-ALT': ['suds'],  # but this should also work
        'SOAP-FALLBACK': ['PySimpleSOAP'],  # this is a fallback
    },
)
