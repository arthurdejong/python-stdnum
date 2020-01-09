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
>>> validate('NL002455799B11')
'002455799B11'
>>> validate('123456789B90')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

import re
import string

from stdnum.exceptions import *
from stdnum.nl import bsn
from stdnum.util import clean, isdigits


# regular expression for matching number
_btw_re = re.compile(r'(?:NL)?[0-9A-Z+*]{10}[0-9]{2}')

# Match letters to integers
_char_to_int = {}
for k in string.ascii_uppercase:
    _char_to_int[k] = str(ord(k) - 55)
_char_to_int['+'] = '36'
_char_to_int['*'] = '37'


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('NL'):
        number = number[2:]
    return bsn.compact(number[:-3]) + number[-3:]


def validate(number):
    """Check if the number is a valid BTW number. Two possible checks:
    - For natural persons
    - For non-natural persons and combinations of natural persons (company)"""
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not _btw_re.match(number):
        raise InvalidFormat()

    # Natural person => mod97 full checksum
    check_val_natural = '2321'
    for x in number:
        check_val_natural += x if isdigits(x) else _char_to_int[x]
    if int(check_val_natural) % 97 == 1:
        return number

    # Company => weighted(9->2) mod11 on bsn
    if isdigits(number[:9]) and number[9] == 'B' and int(number[10:]) > 0:
        bsn.validate(number[:9])
    else:
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid BTW number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
