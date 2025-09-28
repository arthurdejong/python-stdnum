# ogm_vcs.py - functions for handling Belgian OGM-VCS
# coding: utf-8
#
# Copyright (C) 2025 Cédric Krier
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

"""Belgian OGM-VCS.

The OGM-VCS is used in bank transfer as structured communication.

* https://febelfin.be/en/publications/2023/febelfin-banking-standards-for-online-banking

>>> compact('+++010/8068/17183+++')
'010806817183'
>>> validate('+++010/8068/17183+++')
'010806817183'
>>> validate('foo')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('010/8068/1718')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('010/8068/17180')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> is_valid('010/8068/17183')
True
>>> is_valid('010/8068/17180')
False
>>> format('010806817183')
'010/8068/17183'
>>> checksum('0108068171')
83
>>> calc_check_digit('0108068171')
'83'
"""

from __future__ import annotations

from stdnum.exceptions import (
    InvalidChecksum, InvalidFormat, InvalidLength, ValidationError)
from stdnum.util import clean, isdigits


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the number
    of any invalid separators and removes surrounding whitespace."""
    return clean(number, ' +/').strip()


def checksum(number: str) -> int:
    """Calculate the checksum."""
    return (int(number) % 97) or 97


def calc_check_digit(number: str) -> str:
    """Calculate the check digit that should be added."""
    return '%02d' % checksum(number)


def validate(number: str) -> str:
    """Check if the number is a valid OGM-VCS."""
    number = compact(number)
    if not isdigits(number) or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 12:
        raise InvalidLength()
    if checksum(number[:-2]) != int(number[-2:]):
        raise InvalidChecksum()
    return number


def is_valid(number: str) -> bool:
    """Check if the number is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number: str) -> str:
    """Format the number provided for output."""
    number = compact(number)
    number = number.rjust(12, '0')
    return f'{number[:3]}/{number[3:7]}/{number[7:]}'
