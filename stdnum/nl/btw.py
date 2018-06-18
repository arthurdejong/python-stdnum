# btw.py - functions for handling Dutch VAT numbers
#
# Copyright (C) 2012, 2013 Arthur de Jong
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

"""Btw-nummer (Omzetbelastingnummer, the Dutch VAT number).

The btw-nummer is the Dutch number for VAT. It consists of a RSIN or BSN
followed by the letter B and two digits that identify the unit within the
organisation (usually 01).

More information:

* https://en.wikipedia.org/wiki/VAT_identification_number
* https://nl.wikipedia.org/wiki/Btw-nummer_(Nederland)

>>> validate('004495445B01')
'004495445B01'
>>> validate('NL4495445B01')
'004495445B01'
>>> validate('123456789B90')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.exceptions import *
from stdnum.nl import bsn
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('NL'):
        number = number[2:]
    return bsn.compact(number[:-3]) + number[-3:]


def validate(number):
    """Check if the number is a valid BTW number. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not number[10:].isdigit() or int(number[10:]) <= 0:
        raise InvalidFormat()
    if len(number) != 12:
        raise InvalidLength()
    if number[9] != 'B':
        raise InvalidFormat()
    bsn.validate(number[:9])
    return number


def is_valid(number):
    """Check if the number is a valid BTW number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
