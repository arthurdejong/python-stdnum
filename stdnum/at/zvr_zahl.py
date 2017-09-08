# zvr_zahl.py - functions for handling Austrian association register numbers
# coding: utf-8
#
# Copyright (C) 2017 Holvi Payment Services Oy
# Copyright (C) 2017 Arthur de Jong
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
""" ZVR-Zahl (Zentrales Vereinsregister Zahl or ZVR-Zahl or
association registery number)
The number is givin to associations by the Association register to identify
with. The number is 9 character long and is givin on a running bases.
No known checksum, this module will just check if it is clean and all digits.
>>> validate('123456789')
'123456789'
>>> validate('0123456789')
Traceback (most recent call last):
    ...
InvalidLength: ...
validate('A12345678')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> is_valid('123456789')
True
>>> is_valid('1234567890')
False
"""
from stdnum.exceptions import (
    InvalidLength,
    InvalidFormat,
    ValidationError
)
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This removes
    surrounding whitespace and raise an error on junk letters."""
    return clean(number, ' ').strip()


def validate(number):
    """Checks to see if the number provided is a valid association register
    number.
    This checks only the formatting."""
    number = compact(number)
    if len(number) > 9:
        raise InvalidLength()
    if not number.isdigit():
        raise InvalidFormat()
    return number


def is_valid(number):
    """Return boolean value of the association registery number validity"""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
