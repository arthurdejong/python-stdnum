# registrikood.py - functions for handling Estonian Registeration numbers(TIN)
# coding: utf-8
# Copyright (C) 2017 Holvi Payment Services
# Copyright (C) 2015 Arthur de Jong
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
"""registrikood (Legal person TIN, Estonian registeration code).

>>> is_valid('12345678')
True
>>> is_valid('123456789')
False
>>> is_valid('1234567A')
False
>>> validate('12345678')
'12345678'
>>> validate('1234567A')  # incorrect last charicter
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""
from stdnum.exceptions import (
    InvalidFormat,
    InvalidLength,
    ValidationError
)
from stdnum.util import clean


def compact(number):
    """
    Convert the number to the minimal representation. This strips the
    number of any valid separators ' -./,' and removes surrounding whitespace.
    """
    return clean(number, ' ').strip()


def validate(number):
    """Checks if the number provided is valid. This checks the length,
    and check digit."""
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 8:
        raise InvalidLength()
    return number


def is_valid(number):
    """
    Checks if the number provided is valid. This checks the length,
    and check digit.
    """
    try:
        return bool(validate(number))
    except ValidationError:
        return False
