# tfn.py - functions for handling Australian Tax File Numbers (TFNs)
#
# Copyright (C) 2016 Vincent Bastos
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

"""TFN.

>>> validate('876 543 210')
'876543210'
>>> validate('999 999 999')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

import operator

from stdnum.exceptions import *


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = number.replace(" ", "")
    return number


def checksum(number):
    """Calculate the checksum."""
    weights(1, 4, 3, 7, 5, 8, 6, 9, 10)
    return sum(map(operator.mul, number, weights)) % 11


def validate(number):
    """Checks to see if the number provided is a valid TFN number. This checks
    the length, formatting and check digit."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    if checksum(number) != 0:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid TFN number. This checks
    the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

def format(number):
        return "{}{}{} {}{}{} {}{}{}".format(*number)
