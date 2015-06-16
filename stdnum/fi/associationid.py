# associationid.py - functions for handling Finnish association registry id
# coding: utf-8
#
# Copyright (C) 2015 Holvi Payment Services Oy
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

""" Finnish Association Identifier

The number consists of 1 to 6 digits that are normally separated with a dot
in groups of 0-3 and 0-3 numbers. E.g. 123.123, 12.123, 1.123, 123 or 1

>>> businessid.validate('123.123')
u'123.123'

>>> businessid.validate('1123')
u'1.123'

>>> businessid.validate('123123123')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidLength: The number has an invalid length.

>>> businessid.validate('12df')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.

"""

import re
from stdnum.exceptions import *
from stdnum.util import clean


def validate(number):
    """
    Validate the format of a Finnish association register number.

    First strip all separators and spaces from the number and then checks
    that it has a correct length and is only numeric.
    """
    number = clean(number, ' -._+').strip()

    if not number.isdigit():
        raise InvalidFormat()

    if len(number) < 1 or len(number) > 6:
        raise InvalidLength()

    if len(number) < 4:
        return number
    else:
        return "%s.%s" % (number[:-3], number[-3:])


def is_valid(number):
    """Checks to see if the number provided is a valid association register number.
    This checks that the format is correct."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
