# postal_code.py - functions for handling Spanish postal code numbers
# coding: utf-8
#
# Copyright (C) 2023 Víctor Ramos
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

"""Postcode (the Spanish postal code).

They consist of five numerical digits,[2] where the first two digits,
ranging 01 to 52, correspond either to one of the 50 provinces of
Spain or to one of the two autonomous cities on the African coast.

More information:

* https://en.wikipedia.org/wiki/Postal_codes_in_Spain

>>> validate('01000')
'01000'
>>> validate('52000')
'52000'
>>> validate('00000')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('53000')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('99999')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('5200')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('520000')
Traceback (most recent call last):
    ...
InvalidLength: ...
"""


import re

from stdnum.exceptions import *
from stdnum.util import clean


_CP_REGEX = re.compile(r'^(?:0[1-9]|[1-4]\d|5[0-2])\d{3}$')


def compact(number):
    """Convert the number to the minimal representation."""
    return clean(number, ' ').strip()


def validate(number):
    """Check if the number provided is a valid CAS RN."""
    number = compact(number)
    if len(number) != 5:
        raise InvalidLength()
    if not _CP_REGEX.match(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number provided is a valid CAS RN."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
