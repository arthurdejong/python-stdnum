# ico.py - functions for handling Czech organisation identifiers
# coding: utf-8
#
# Copyright (C) 2026 Devashish Moghe
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

"""IČO (Identifikační číslo osoby, Czech organisation identifier).

The IČO (Identifikační číslo osoby, also abbreviated IČ) is an 8-digit
number (including a trailing check digit) that uniquely identifies a legal
entity or sole trader registered in the Czech Republic. It is assigned by
the Czech Statistical Office and is listed in the public business register
(ARES).

The number is the same as the digits of the legal entity's Czech VAT number
(DIČ, see stdnum.cz.dic) without the ``CZ`` prefix.

More information:

* https://cs.wikipedia.org/wiki/Identifikační_číslo_osoby
* https://ares.gov.cz/

>>> validate('00177041')
'00177041'
>>> validate('001 77 041')
'00177041'
>>> validate('00177042')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('0017704')  # too short
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('0017704X')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from __future__ import annotations

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' /').strip()


def calc_check_digit(number: str) -> str:
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    # weighted modulo 11 checksum; this is the same algorithm used for the
    # 8-digit (legal entity) form of the Czech DIČ, see stdnum.cz.dic
    check = (11 - sum((8 - i) * int(n) for i, n in enumerate(number))) % 11
    return str((check or 1) % 10)


def validate(number: str) -> str:
    """Check if the number is a valid IČO. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 8:
        raise InvalidLength()
    if number[-1] != calc_check_digit(number[:-1]):
        raise InvalidChecksum()
    return number


def is_valid(number: str) -> bool:
    """Check if the number is a valid IČO."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
