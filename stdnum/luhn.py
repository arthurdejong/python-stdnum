# luhn.py - functions for performing the Luhn and Luhn mod N algorithms
#
# Copyright (C) 2010-2021 Arthur de Jong
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

"""The Luhn and Luhn mod N algorithms.

The Luhn algorithm is used to detect most accidental errors in various
identification numbers.

>>> validate('7894')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> checksum('7894')
6
>>> calc_check_digit('7894')
'9'
>>> validate('78949')
'78949'

An alternative alphabet can be provided to use the Luhn mod N algorithm.
The default alphabet is '0123456789'.

>>> validate('1234', alphabet='0123456789abcdef')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> checksum('1234', alphabet='0123456789abcdef')
14
"""
from __future__ import annotations

from stdnum.exceptions import *


def checksum(number: str, alphabet: str = '0123456789') -> int:
    """Calculate the Luhn checksum over the provided number. The checksum
    is returned as an int. Valid numbers should have a checksum of 0."""
    n = len(alphabet)
    digits = tuple(alphabet.index(i)
                   for i in reversed(str(number)))
    return (sum(digits[::2]) +
            sum(sum(divmod(i * 2, n))
                for i in digits[1::2])) % n


def validate(number: str, alphabet: str = '0123456789') -> str:
    """Check if the number provided passes the Luhn checksum."""
    if not bool(number):
        raise InvalidFormat()
    try:
        valid = checksum(number, alphabet) == 0
    except Exception:  # noqa: B902
        raise InvalidFormat()
    if not valid:
        raise InvalidChecksum()
    return number


def is_valid(number: str, alphabet: str = '0123456789') -> bool:
    """Check if the number passes the Luhn checksum."""
    try:
        return bool(validate(number, alphabet))
    except ValidationError:
        return False


def calc_check_digit(number: str, alphabet: str = '0123456789') -> str:
    """Calculate the extra digit that should be appended to the number to
    make it a valid number."""
    ck = checksum(str(number) + alphabet[0], alphabet)
    return alphabet[-ck]
