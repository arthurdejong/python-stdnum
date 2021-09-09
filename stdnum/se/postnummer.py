# postcode.py - functions for handling Swedish postal codes
#
# Copyright (C) 2021 Michele Ciccozzi
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

"""Postcode (the Swedish postal code).

The Swedish postal code consists of three numbers followed by two letters,
separated by a single space.

More information:
* https://en.wikipedia.org/wiki/Postal_codes_in_Sweden
* https://sv.wikipedia.org/wiki/Postnummer_i_Sverige

>>> format('114 18')
'114 18'
>>> validate('114 18')
11418
>>> validate('SE-11418')
11418
>>> validate('1145 18')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


_postcode_re = re.compile(r'^(?P<pt1>[1-9][0-9]{2})(?P<pt2>[0-9]{2})$')


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    if not isinstance(number, str):
        number = str(number)
    number = clean(number, ' -').upper().strip()
    if number.startswith('SE'):
        number = number[2:]
    return number


def validate(number):
    """Check if the number is in the correct format. This currently does not
    check whether the code corresponds to a real address."""
    number = compact(number)
    match = _postcode_re.search(number)
    if not match:
        raise InvalidFormat()
    return int(number)


def is_valid(number):
    """Check if the number is a valid postal code."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    if is_valid(number):
        number = compact(number)
        match = _postcode_re.search(number)
        return '%s %s' % (match.group('pt1'), match.group('pt2'))
    else:
        raise InvalidFormat()
