# aadhaar.py - functions for handling Indian Aadhaar numbers
#
# Copyright (C) 2017 Srikanth L
# Copyright (C) 2021 Gaurav Chauhan
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

"""Aadhaar (Indian digital resident personal identity number)

Aadhaar is a 12 digit unique identity number issued to all Indian residents.
The number is assigned by the Unique Identification Authority of India
(UIDAI).

Aadhaar is made up of 12 numeric characters, a unique 11 digit number and one
check digit calculated using Verhoeff algorithm. The number is generated
random, non-repeating sequence and does not begin with 0 or 1.

More information:

* https://en.wikipedia.org/wiki/Aadhaar
* https://web.archive.org/web/20140611025606/http://uidai.gov.in/UID_PDF/Working_Papers/A_UID_Numbering_Scheme.pdf

>>> validate('234123412346')
'234123412346'
>>> validate('643343121')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('123412341234')  # number should not start with 0 or 1
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('234123412347')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('234123412346')
'2341 2341 2346'
>>> mask('234123412346')
'XXXX XXXX 2346'
"""

import re
import stdnum.exceptions as e

from stdnum import verhoeff
from stdnum.util import clean


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""

    return clean(number, " -").strip()


def validate(number: str) -> str:
    """Check if the number provided is a valid Aadhaar number. This checks
    the length, formatting and check digit."""

    AADHAAR_RE = re.compile(r"^[2-9][0-9]{11}$")
    number = compact(number)
    if len(number) != 12:
        raise e.InvalidLength()
    if not AADHAAR_RE.match(number):
        raise e.InvalidFormat()
    verhoeff.validate(number)
    return number


def is_valid(number: str) -> bool:
    """Check if the number provided is a valid Aadhaar number. This checks
    the length, formatting and check digit."""

    try:
        return bool(validate(number))
    except e.ValidationError:
        return False


def format(number: str) -> str:
    """Reformat the number to the standard presentation format."""

    number = compact(number)
    return " ".join((number[:4], number[4:8], number[8:]))


def mask(number: str) -> str:
    """Masks the first 8 digits as per Ministry of Electronics and
    Information Technology (MeitY) guidelines."""

    number = compact(number)
    return "XXXX XXXX " + number[-4:]
