# orgnr.py - functions for handling Swedish organization numbers
# coding: utf-8
#
# Copyright (C) 2012, 2013 Arthur de Jong
# Copyright (C) 2014 Tomas Thor Jonsson
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

"""Orgnr (Organisationsnummer, Swedish company number).

The Orgnr (Organisationsnummer) is the national number to identify
Swedish companies and consists of 10 digits. These are the first
10 digits in the Swedish VAT number, i.e. it's the VAT number
without the 'SE' in front and the '01' at the end.

>>> validate('SE 123456789701')
'123456789701'
>>> validate('123456789101')  # invalid check digits
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum import luhn
from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('SE'):
        number = number[2:]
    return number


def validate(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 10:
        raise InvalidLength()
    luhn.validate(number[:-2])
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
