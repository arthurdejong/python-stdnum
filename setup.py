#!/usr/bin/env python

# setup.py - python-stdnum installation script
#
# Copyright (C) 2010-2014 Arthur de Jong
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
from setuptools import setup, find_packages

import stdnum

# fix permissions for sdist
if 'sdist' in sys.argv:
    os.system('chmod -R a+rX .')
    os.umask(int('022', 8))

setup(name='python-stdnum',
      version=stdnum.__version__,
      description='Python module to handle standardized numbers and codes',
      long_description=stdnum.__doc__,
      author='Arthur de Jong',
      author_email='arthur@arthurdejong.org',
      url='http://arthurdejong.org/python-stdnum/',
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
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing :: General',
          ],
      packages=find_packages(),
      package_data={'': ['*.dat']},
      extras_require={
          'VIES':  ['suds'],
          },
      )
