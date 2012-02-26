# isil.py - functions for handling identifiers for libraries and related
#           organizations
#
# Copyright (C) 2011 Arthur de Jong
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

>>> is_valid('IT-RM0267')
True
>>> is_valid('OCLC-DLC')
True
>>> is_valid('WW-RM0267') # unregistered country code
False
>>> format('it-RM0267')
'IT-RM0267'
"""

# the valid characters in an ISIL
_alphabet = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-:/')


def compact(number):
    """Convert the ISIL to the minimal representation. This strips
    surrounding whitespace."""
    return number.strip()


def _known_agency(agency):
    """Checks whether the specified agency is valid."""
    # look it up in the db
    from stdnum import numdb
    results = numdb.get('isil').info(agency.upper() + '$')
    # there should be only one part and it should have properties
    return len(results) == 1 and bool(results[0][1])


def is_valid(number):
    """Checks to see if the number provided is a valid isil (or isilSV)
    number."""
    try:
        number = compact(number)
    except:
        return False
    for n in number:
        if n not in _alphabet:
            return False
    return len(number) <= 15 and _known_agency(number.split('-')[0])


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    parts = number.split('-')
    if len(parts) > 1 and _known_agency(parts[0]):
        parts[0] = parts[0].upper()
    return '-'.join(parts)
