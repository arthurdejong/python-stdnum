# accise.py - functions for handling French Accise numbers
# coding: utf-8
#
# Copyright (C) 2023 Cédric Krier
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

"""n° d'accise (French number to identify taxpayers of excise taxes).

The n° d'accise always start by FR0 following by the 2 ending digits of the
year, 3 number of customs office, one letter for the type and an ordering
number of 4 digits.

>>> compact('FR0 23 004 N 9448')
'FR023004N9448'
>>> validate('FR023004N9448')
'FR023004N9448'
>>> validate('FR012907E0820')
'FR012907E0820'

>>> validate('FR012345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('FR0XX907E0820')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('FR012XXXE0820')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('FR012907A0820')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('FR012907EXXXX')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


OPERATORS = set(['E', 'N', 'C', 'B'])


def compact(number):
    """Convert the number to the minimal representation. This strips the number
    of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    return number


def validate(number):
    """Check if the number is a valid accise number. This checks the length,
    formatting."""
    number = clean(number, ' ').upper().strip()
    code = number[:3]
    if code != 'FR0':
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()
    if not isdigits(number[3:5]):
        raise InvalidFormat()
    if not isdigits(number[5:8]):
        raise InvalidFormat()
    if number[8] not in OPERATORS:
        raise InvalidFormat()
    if not isdigits(number[9:12]):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid accise number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
