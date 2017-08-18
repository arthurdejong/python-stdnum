# veronumero.py - functions for handling Finnish tax numbers
# coding: utf-8
#
# Copyright (C) 2012-2015 Arthur de Jong
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

"""
Veronumero (Finnish tax number).

Module for handling veronumero (Finnish Tax numbers).
See
https://www.vero.fi/en/detailed-guidance/guidance/48791/individual_tax_numbers__instructions_fo/
There is no checksum for this identifier.

>>> validate('123456789123')
'123456789123'
>>> validate('12345678912A')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('123456789')
Traceback (most recent call last):
    ...
InvalidInvalidLength: ...
"""
from stdnum.exceptions import (
    InvalidFormat,
    InvalidLength,
    ValidationError
)


def validate(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 12:
        raise InvalidLength()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
