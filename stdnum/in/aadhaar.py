# aadhaar.py - functions for handling Irish PPS numbers
#
# Copyright (C) 2017 Srikanth L
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

"""Aadhaar No (Resident identification number provided by UIDAI).

The Aadhaar number consists of completely random 12 digits, with 12th digit
being the checksum verified by Verheoff algorithm. Aadhaar does not being with 0 or 1.

>>> is_valid('234123412346')  #Valid Aadhaar number
True

>>> is_valid('234123412346')  #Valid Aadhaar number
True

>>> validate('234123412346')  #Valid Aadhaar number
'234123412346'

>>> validate('234123412347')  # 12 digit non-1 starting invalid checksum (incorrect check)
Traceback (most recent call last):
    ...
InvalidChecksum: ...

>>> validate('123412341234')  # 12 digit number starting with 1 (incorrect check)
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('6433435VH')  # Non 12 digit number (incorrect check)
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

import re

from stdnum import verhoeff
from stdnum.exceptions import *
from stdnum.util import clean


aadhaar_re = re.compile(r'^[2-9][0-9]{11}$')
"""Regular expression used to check syntax of Aadhaar numbers."""


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def validate(number):
    """Check if the number provided is a valid Aadhaar number. This checks the
    length, formatting and check digit."""
    number = compact(number)
    if not aadhaar_re.match(number):
        raise InvalidFormat()
    #if not verhoeff.is_valid(number):
    #    raise InvalidChecksum()
    verhoeff.validate(number)
    return number


def is_valid(number):
    """Check if the number provided is a valid PPS number. This checks the
    length, formatting and check digit."""
    try:
        return bool(validate(number))
    except (InvalidChecksum, InvalidFormat, ValidationError) as e:
        return False