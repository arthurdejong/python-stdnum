# blz.py - functions for handling German bank codes
# coding: utf-8
#
# Copyright (C) 2026 Claude-Alain Martin
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

"""BLZ (Bankleitzahl, German bank code).

The Bankleitzahl is an 8 digit number that identifies a bank (or a branch
that takes part in payment transactions) in Germany. It is found in
positions 5 to 12 of a German IBAN. The Deutsche Bundesbank publishes the
register of allocated codes with the institution, its BIC and its place,
and marks codes that are about to be deleted, with the successor code where
one exists.

More information:

* https://en.wikipedia.org/wiki/Bankleitzahl
* https://www.bundesbank.de/de/aufgaben/unbarer-zahlungsverkehr/serviceangebot/bankleitzahlen

>>> validate('10000000')
'10000000'
>>> validate('370 400 44')
'37040044'
>>> import json
>>> print(json.dumps(info('10000000'), indent=2, sort_keys=True))
{
  "bank": "Bundesbank",
  "bic": "MARKDEF1100",
  "city": "Berlin"
}
>>> to_bic('37040044')
'COBADEFFXXX'
>>> validate('12345678')  # not allocated
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('1234567')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('ABCDEFGH')
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
    return clean(number, ' ').strip()


def info(number: str) -> dict[str, str]:
    """Return a dictionary of data about the supplied number. This typically
    returns the name of the bank, its BIC and its place, and for a code that
    is about to be deleted the successor code where one exists."""
    number = compact(number)
    from stdnum import numdb
    return numdb.get('de/banks').info(number)[0][1]


def to_bic(number: str) -> str | None:
    """Return the BIC for the bank that this number refers to."""
    return info(number).get('bic')


def validate(number: str) -> str:
    """Check if the number is a valid bank code. This checks the format and
    whether the code is allocated in the register of the Deutsche
    Bundesbank."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 8:
        raise InvalidLength()
    if not info(number):
        raise InvalidComponent()
    return number


def is_valid(number: str) -> bool:
    """Check if the number is a valid bank code."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
