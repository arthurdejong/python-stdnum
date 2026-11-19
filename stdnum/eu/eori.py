# eori.py - functions for handling Economic Operators Registration and Identification numbers
# coding: utf-8
#
# Copyright (C) 2026 Sergi Almacellas Abellana
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

"""EORI (Economic Operators Registration and Identification number).

An EORI number identifies economic operators in customs procedures. It starts
with a two-letter country code followed by up to 15 alphanumeric characters.
This module validates only the common EORI format; national EORI formats are
not checked.

More information:

* https://taxation-customs.ec.europa.eu/customs/customs-procedures-import-and-export/customs-operations/economic-operators-registration-and-identification-number-eori_en  # noqa: E501

>>> validate('ES B64717838')
'ESB64717838'
>>> validate('ESB12345678!')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from __future__ import annotations

from string import ascii_uppercase, digits

from stdnum.exceptions import *
from stdnum.util import clean


_alphabet = ascii_uppercase + digits


def compact(number: str) -> str:
    """Convert the number to the minimal representation."""
    return clean(number, ' -').strip().upper()


def validate(number: str) -> str:
    """Check if the number has a valid EORI format."""
    number = compact(number)
    if not 3 <= len(number) <= 17:
        raise InvalidLength()
    if (not all(x in ascii_uppercase for x in number[:2]) or
            not all(x in _alphabet for x in number[2:])):
        raise InvalidFormat()
    return number


def is_valid(number: str) -> bool:
    """Check if the number has a valid EORI format."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
