#!/usr/bin/env python

# setup.py - python-stdnum installation script
#
# Copyright (C) 2010 Arthur de Jong
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
from setuptools import setup, find_packages

setup(name='python-stdnum',
      version='0.1',
      packages=find_packages(),
      author='Arthur de Jong',
      author_email='arthur@arthurdejong.org',
      url='http://arthurdejong.org/python-stdnum',
      license='LGPL',
      description='Python module to handle standardized numbers and codes',
      long_description= \
          """A Python module to parse, validate and reformat standard numbers
          and codes in different formats.

          Currently this module supports the following formats:

           * ISBN (International Standard Book Number)
           * ISSN (International Standard Serial Number)
           * BSN (Burgerservicenummer, the Dutch national identification number)
          """,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing :: General',
          ],
      )
