# orgnr.py - functions for handling Norwegian organization numbers
# coding: utf-8
#
# Copyright (C) 2012, 2013 Arthur de Jong
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

"""Orgnr (Organisasjonsnummer, Norwegian organization number).

The number is 9-digit code where the last digit is a weighted MOD11
checksum.

>>> validate('995525828')
'995525828'
>>> validate('995525829')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    return number


def checksum(number):
    """Calculate the checksum."""
    weights = (3, 2, 7, 6, 5, 4, 3, 2)
    return 11 - sum(weights[i] * int(n) for i, n in enumerate(number)) % 11


def validate(number):
    """Checks to see if the number provided is a valid organization
    number. This checks the length, formatting and check digit."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    if checksum(number[:8]) != int(number[8]):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid organization
    number. This checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
