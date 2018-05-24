# structured_creditor_reference.py - functions for performing the ISO 11649
# checksum validation for structured creditor reference numbers.
#
# Copyright (C) 2018 Esben Toke Christensen
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

"""The ISO 11649 structured creditor reference number consists of 'RF' followed
by two check digits and a number of 1-21 digits. The number
may contain letters.

The reference number is validated by moving RF and the check digits to the end
of the number, and checking that the iso7064 mod_97_10 checksum of this string
is 1.

>>> validate('RF18 5390 0754 7034')
'RF18539007547034'
>>> validate('RF18 5390 0754 70Y')
'RF185390075470Y'
>>> is_valid('RF18 5390 0754 7034')
True
>>> validate('RF17 5390 0754 7034')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.util import clean
from stdnum.exceptions import *
import stdnum.iso7064.mod_97_10 as mod_97_10


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any invalid separators and removes surrounding whitespace."""
    return clean(number, ' -.,/:').upper().strip()


def checksum(number):
    """Calculate the checksum."""
    return mod_97_10.checksum(number[4:] + number[:4])


def validate(number):
    """Check if the number provided is a valid iso11649 structured creditor
    reference number."""
    number = compact(number)
    if len(number) < 5 or len(number) > 25:
        raise InvalidLength()
    if number[:2] != 'RF':
        raise InvalidFormat()
    if checksum(number) != 1:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid iso11649 structured creditor
    number. This checks the length, formatting and check digits."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
