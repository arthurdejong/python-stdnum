# bankgiro.py - functions for handling Swedish Bankgiro numbers
# coding: utf-8
#
# Copyright (C) 2026 Gracestack (Kim Cedendahl)
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

"""Bankgiro (Swedish bank giro number).

The Bankgiro number is used in Sweden to identify bank giro accounts
for invoice payments and other bank transfers. The number consists of
7 or 8 digits and includes a check digit calculated using the Luhn
(mod-10) algorithm, which is the same as used by the related PlusGiro
numbers.

Bankgiro numbers are commonly formatted as NNN-NNNN (7 digits) or
NNNN-NNNN (8 digits) with a hyphen separating the groups.

More information:

* https://www.bankgirot.se/en/

>>> validate('9000001')
'9000001'
>>> validate('9000002')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('123456789')  # too long
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('9000001')
'900-0001'
>>> format('50501501')
'5050-1501'
"""

from __future__ import annotations

from stdnum import luhn
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -.').strip()


def validate(number: str) -> str:
    """Check if the number is a valid Bankgiro number. This checks
    the length, formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) not in (7, 8):
        raise InvalidLength()
    return luhn.validate(number)


def is_valid(number: str) -> bool:
    """Check if the number is a valid Bankgiro number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number: str) -> str:
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    if len(number) == 7:
        return number[:3] + '-' + number[3:]
    else:
        return number[:4] + '-' + number[4:]