# acn.py - functions for handling Australian Company Numbers (ACNs)
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

"""ACN.

>>> validate('010 499 966')
'010499966'
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
    weights(8, 7, 6, 5, 4, 3, 2, 1)
    return (10 - (sum(map(operator.mul, number, weights))) % 10) % 10


def validate(number):
    """Checks to see if the number provided is a valid ACN number. This checks
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
    """Checks to see if the number provided is a valid ACN number. This checks
    the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

def format(number):
        return "{}{}{} {}{}{} {}{}{}".format(*number)
