# isil.py - functions for handling identifiers for libraries and related
#           organizations
#
# Copyright (C) 2011, 2012, 2013 Arthur de Jong
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

"""ISIL (International Standard Identifier for Libraries).

The ISIL is the International Standard Identifier for
Libraries and Related Organizations.

>>> validate('IT-RM0267')
'IT-RM0267'
>>> validate('OCLC-DLC')
'OCLC-DLC'
>>> validate('WW-RM0267')  # unregistered country code
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('WW-RM026712423345334534512334534545')  # too long
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('it-RM0267')
'IT-RM0267'
"""

from stdnum.exceptions import *
from stdnum.util import clean


# the valid characters in an ISIL
_alphabet = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-:/')


def compact(number):
    """Convert the ISIL to the minimal representation. This strips
    surrounding whitespace."""
    return clean(number, '').strip()


def _known_agency(agency):
    """Checks whether the specified agency is valid."""
    # look it up in the db
    from stdnum import numdb
    results = numdb.get('isil').info(agency.upper() + '$')
    # there should be only one part and it should have properties
    return len(results) == 1 and bool(results[0][1])


def validate(number):
    """Checks to see if the number provided is a valid isil (or isilSV)
    number."""
    number = compact(number)
    for n in number:
        if n not in _alphabet:
            raise InvalidFormat()
    if len(number) > 15:
        raise InvalidLength()
    if not _known_agency(number.split('-')[0]):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid isil (or isilSV)
    number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    parts = number.split('-')
    if len(parts) > 1 and _known_agency(parts[0]):
        parts[0] = parts[0].upper()
    return '-'.join(parts)
