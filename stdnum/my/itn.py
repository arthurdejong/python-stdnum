# itn.py - functions for handling ITN numbers
#
# Copyright (C) 2020 Sergi Almacellas Abellana
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

"""ITN No. (Malaysian Income Tax Number)

The number is assigned by The Inland Revenue Board of Malaysia (IRBM) and it
is required to report the income. This unique number is known as
"Nombor Cukai Pendapatan" or Income Tax Number (ITN).

For individuals the ITN consists on the 2 letters Type of File Number (SG for
individual resident or OG for individual non-resident) followed by a space, and
ending with the Income Tax Number (maximum 11 digits).

For Non-Individuals the ITN consists on the Type of File Number (1 or 2 letters)
followed by a space, and ending with the Income Tax Number (maximum 10 digits).
The Type of File Number for Non-Individuals can be one of the following:

* C: Company, Pte. Ltd. Company, Limited Company or Non-Resident Company.
* CS: Cooperative Society.
* D: Partnership.
* E: Employer.
* F: Association.
* FA: Non-Resident Public Entertainer.
* PT: Limited Liability Partnership.
* TA: Trust Body.
* TC: Unit Trust/ Property Trust.
* TN: Business Trust.
* TR: Real Estate Investment Trust/ Property Trust Fund.
* TP: Deceased Person's Estate.
* TJ: Hindu Joint Family.
* LE: Labuan Entity.

>>> validate('SG 10234567090')
'SG10234567090'
>>> validate('OG 25845632021')
'OG25845632021'
>>> validate('C 2584563202')
'C2584563202'
>>> validate('1')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('12345678901234')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('X 12345')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('C 12345X')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> format('C2584563202')
'C 2584563202'
>>> format('SG10234567090')
'SG 10234567090'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


PREFIXES_11_DIGITS = ('SG', 'OG')
PREFIXES_10_DIGITS = ('C', 'CS', 'D', 'E', 'F', 'FA', 'PT', 'TA', 'TC', 'TN',
                      'TR', 'TP', 'TJ', 'LE')
VALID_PREFIXES = PREFIXES_11_DIGITS + PREFIXES_10_DIGITS


def _get_prefix_and_number(number):
    """Return the number separated in prefix and numerical part.

    This assumes the number has been previously compacted.
    """
    for i, c in enumerate(number):
        if c.isdigit():
            return number[:i], number[i:]
    return number, ''


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -*').strip().upper()


def validate(number):
    """Check if the number is a valid ITN number.

    This checks the length and formatting.
    """
    number = compact(number)
    prefix, digits = _get_prefix_and_number(number)
    if prefix not in VALID_PREFIXES:
        raise InvalidComponent()
    if not digits:
        raise InvalidComponent()
    if prefix in PREFIXES_11_DIGITS and len(digits) > 11:
        raise InvalidComponent()
    if prefix in PREFIXES_10_DIGITS and len(digits) > 10:
        raise InvalidComponent()
    if not isdigits(digits):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid ITN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return ' '.join(_get_prefix_and_number(compact(number)))
