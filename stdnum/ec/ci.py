# dni.py - functions for handling Ecuadorian personal identity codes
# coding: utf-8
#
# Copyright (C) 2014 Jonathan Finlay
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

"""CI (Cédula de identidad, Ecuadorian personal identity codes).

The CI is a 10 digit number used to identify Ecuadorian citizens.

>>> validate('1714307103')
'1714307103'
>>> validate('171430710-3')
'1714307103'
>>> validate('1714307104')  # invalid document
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('171430710')  # digit missing
Traceback (most recent call last):
    ...
InvalidLength: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def checksum(number):
    """Calculate the check digit."""
    value = [int(number[x]) * (2 - x % 2) for x in range(9)]
    total = sum(map(lambda x: x > 9 and x - 9 or x, value))
    if int(int(number[9] if int(number[9]) != 0 else 10)) != (10 - int(str(total)[-1:])):
        return False
    return True


def validate(number):
    """Checks to see if the number provided is a valid CI number. This
    checks the length, formatting and check digit."""
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not number.isdigit():
        raise InvalidFormat()
    if not checksum(number):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid CI number. This
    checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
