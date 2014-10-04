# ric.py - functions for handling Chinese Resident Identity Card Number
#
# Copyright (C) 2014 Jiangge Zhang
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

"""RIC No. (Chinese Resident Identity Card Number).

The RIC No. is the unique identifier for issued to China (PRC) residents.

The number consist of 18 digits in four sections. The first 6 digits refers to
the resident's location, followed by 8 digits represeting the resident's birth
day in the form YYYY-MM-DD. The next 3 digits is the order code which is the
code used to disambiguate people with the same date of birth and address code.
Men are assigned to odd numbers, women assigned to even numbers. The final
digit is the checksum.

>>> validate('360426199101010071')
'360426199101010071'
>>> validate('36042619910101007V')  # invalid format
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('360426199113010079')  # invalid dates
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('36042619910102009X')  # invalid checksum
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('990426199112010074')  # unknown birth place code
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> format('44011320141005001x')
'44011320141005001X'
"""

import datetime

from stdnum.exceptions import (
    ValidationError, InvalidLength, InvalidFormat, InvalidChecksum,
    InvalidComponent)
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number).upper().strip()


def get_birth_date(number):
    """Split the date parts from the number and return the birth date.
    Note that in some cases it may return the registration date instead of
    the birth date and it may be a century off."""
    number = compact(number)
    year = int(number[6:10])
    month = int(number[10:12])
    day = int(number[12:14])
    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise InvalidComponent()


def get_birth_place(number):
    """Use the number to look up the place of birth of the person."""
    from stdnum import numdb
    number = compact(number)
    results = numdb.get('cn/loc').info(number[:6])[0][1]
    if not results:
        raise InvalidComponent()
    return results


def calc_check_digit(number):
    checksum = (1 - 2 * int(number[:-1], 13)) % 11
    return 'X' if checksum == 10 else str(checksum)


def validate(number):
    """Checks to see if the number provided is a valid RIC numbers. This
    checks the length, formatting and birth date and place."""
    number = compact(number)
    if len(number) != 18:
        raise InvalidLength()
    if not number[:-1].isdigit():
        raise InvalidFormat()
    if not number[-1].isdigit() and number[-1] != 'X':
        raise InvalidFormat()
    if number[-1] != calc_check_digit(number):
        raise InvalidChecksum()
    get_birth_date(number)
    get_birth_place(number)
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid RIC numbers. This
    checks the length, formatting and birth date and place."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the passed number to the standard format."""
    return compact(number)
