# vat.py - functions for handling Irish VAT numbers
#
# Copyright (C) 2012, 2013 Arthur de Jong
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

"""VAT (Irish VAT number).

The Irish VAT number consists of 8 digits. The last digit is a check
letter, the second digit may be a number, a letter, "+" or "*".

>>> validate('IE 6433435F')  # pre-2013 format
'6433435F'
>>> validate('IE 6433435OA')  # 2013 format
'6433435OA'
>>> validate('6433435E')  # incorrect check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('8D79739I')  # old style number
'8D79739I'
>>> validate('8?79739J')  # incorrect old style
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('IE'):
        number = number[2:]
    return number


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    alphabet = 'WABCDEFGHIJKLMNOPQRSTUV'
    number = compact(number).zfill(7)
    return alphabet[(
        sum((8 - i) * int(n) for i, n in enumerate(number[:7])) +
        9 * alphabet.index(number[7:])) % 23]


def validate(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    number = compact(number)
    if not number[:1].isdigit() or not number[2:7].isdigit():
        raise InvalidFormat()
    if len(number) not in (8, 9):
        raise InvalidLength()
    if number[:7].isdigit():
        # new system
        if number[7] != calc_check_digit(number[:7] + number[8:]):
            raise InvalidChecksum()
    elif number[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ+*':
        # old system
        if number[7] != calc_check_digit(number[2:7] + number[0]):
            raise InvalidChecksum()
    else:
        raise InvalidFormat()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
