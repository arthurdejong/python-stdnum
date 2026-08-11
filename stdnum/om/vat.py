# vat.py - functions for handling Oman VAT numbers
# coding: utf-8
#
# Copyright (C) 2026 Devashish Moghe
# Copyright (C) 2026 Arthur de Jong
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

"""VAT (Oman value added tax number).

The Oman VAT identification number (VATIN) is issued by the Oman Tax
Authority to businesses registered for value added tax. It consists of the
letters ``OM`` followed by 10 digits (12 characters in total).

There is no check digit; a number can be verified online through the Oman
Tax Authority portal.

More information:

* https://tms.taxoman.gov.om/portal/vat-tax
* https://tms.taxoman.gov.om/portal/vatin-validation

>>> validate('OM1100006083')
'OM1100006083'
>>> validate('OM1100006084')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('OM 1100 0060 83')
'OM1100006083'
>>> validate('110000608312')  # missing prefix
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('OM110000608')  # too short
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('OM11000060AB')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from __future__ import annotations

import re

from stdnum.exceptions import *
from stdnum.util import clean


# the VATIN consists of the OM prefix followed by ten digits
_vatin_re = re.compile(r'^OM[0-9]{9}[0-9X]$')


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def calc_check_digit(number: str) -> str:
    """Calculate the check digit."""
    # We only know the weights of the last 5 digits so we skip the first 4
    weights = (1, 6, 3, 7, 9)
    check = (1 + sum(w * int(n) for w, n in zip(weights, number[6:]))) % 11
    return 'X' if check == 10 else str(check)


def validate(number: str) -> str:
    """Check if the number is a valid Oman VAT number. This checks the
    length and formatting."""
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not _vatin_re.match(number):
        raise InvalidFormat()
    if calc_check_digit(number) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number: str) -> bool:
    """Check if the number is a valid Oman VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
