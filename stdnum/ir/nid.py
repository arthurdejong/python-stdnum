# nid.py - functions for handling Iranian national identification numbers
# coding: utf-8
#
# Copyright (C) 2026 Amir Douzandeh
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
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

"""National ID Number (Iranian national identification number).

The Iranian National ID Number (Code Melli) is a 10-digit number assigned to
every Iranian citizen. The last digit is a check digit. Leading zeros are
significant but are often lost when the number is stored as an integer, so
numbers of 8 or 9 digits are padded with zeros.

More information:

* https://en.wikipedia.org/wiki/National_identification_number#Iran

>>> validate('0499370899')
'0499370899'
>>> validate('84575948')  # leading zeros are restored
'0084575948'
>>> validate('0499370898')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('04993708')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('049937')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('1111111111')  # repeated digits are never valid
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from __future__ import annotations

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators, removes surrounding whitespace and pads
    numbers of 8 or 9 digits with leading zeros to 10 digits."""
    number = clean(number, ' -').strip()
    if isdigits(number) and 8 <= len(number) < 10:
        number = number.zfill(10)
    return number


def calc_check_digits(number: str) -> str:
    """Calculate the check digit for the specified number. The number
    passed should not have the check digit included."""
    remainder = sum(
        int(n) * w for n, w in zip(number[:9], range(10, 1, -1))) % 11
    return str(remainder if remainder < 2 else 11 - remainder)


def validate(number: str) -> str:
    """Check if the number is a valid Iranian national ID number. This
    checks the length, formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    if len(set(number)) == 1:
        raise InvalidFormat()
    if calc_check_digits(number) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number: str) -> bool:
    """Check if the number is a valid Iranian national ID number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
