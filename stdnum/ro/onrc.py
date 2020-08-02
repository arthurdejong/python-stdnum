# onrc.py - functions for handling Romanian ONRC numbers
# coding: utf-8
#
# Copyright (C) 2020 Dimitrios Josef Moustos
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

from stdnum.exceptions import *
from stdnum.util import clean, isdigits
import datetime
import re

"""ONRC (Numarul de ordine din registrul comertului).

The ONRC number is a 9-14 character string containing information
about the type of company, county, sequence number, 4 char year,
separated by /. The EUID identifier is based on this number.

>>> validate('J52/750/22.11.2012')  # valid, strip date, leave year
'J52/750/2012'

>>> validate('X52/750/2012')  # invalid first (type) character
Traceback (most recent call last):
    ...
>>> validate('J49/750/2012')  # first number is invalid county no
Traceback (most recent call last):
    ...
>>> validate('J52/100000/2012') # second number too large
    ...
>>> validate('J52/750/3000') # last number (year) is in the future
Traceback (most recent call last):"""

# regular expression to check ONRC structure
_onrc_re = re.compile(r'^[JFC](?P<county>[1-9]\d?)\/(?P<n>[1-9]\d{0,4})\/(?P<year>\d{4})$')
_current_year=datetime.datetime.now().year

def compact(number):
	"""Strip the number of some unwanted characters. On the registration
	certificate the format is J52/750/22.11.2012, which is not the right
	storage format, we convert it to J50/750/2012"""
	number = clean(number, ' -').upper().strip()
	if 15 <= len(number) <= 20:
		number = number[0:len(number)-10] + number[len(number)-4:len(number)]
	return number

def validate(number):
	"""Check if the identifier is valid by checking formatting by re,
	first character (company type), county number, sequence number range,
	year between 1990 and current year."""
	number=compact(number)
	match = _onrc_re.search(number)
	if not match: raise InvalidFormat()
	if (int(match.group('county')) > 40):
		if not 51 <= int(match.group('county')) <= 52:
				raise InvalidComponent()
	if not 1990 <= int(match.group('year')) <= _current_year:
		raise InvalidComponent()
	return number

def is_valid(number):
    """Check if the number is a valid ONRC identifier."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
