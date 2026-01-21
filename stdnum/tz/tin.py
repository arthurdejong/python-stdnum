# tin.py - functions for handling Tanzania TIN numbers
# coding: utf-8
#
# Copyright (C) 2023 Leandro Regueiro
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

"""TIN (Taxpayer Identification Number, or TIN namba, Tanzania tax number).

This number consists of 9 digits, usually separated into three groups
using hyphens to make it easier to read, like XXX-XXX-XXX.

>>> validate('121-207-079')
'121207079'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('121207079')
'121-207-079'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return str(clean(number, u' -–').strip())


def validate(number):
    """Check if the number is a valid Tanzania TIN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Tanzania TIN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join([number[:3], number[3:-3], number[-3:]])
