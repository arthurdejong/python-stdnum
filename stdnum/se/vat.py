# vat.py - functions for handling Swedish VAT numbers
# coding: utf-8
#
# Copyright (C) 2012 Arthur de Jong
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

"""VAT (Moms, Mervärdesskatt, Swedish VAT number).

The Momsregistreringsnummer is used for VAT (Moms, Mervärdesskatt)
purposes and consists of 12 digits of which the last two should be 01. The
first 10 digits should have a valid Luhn checksum.

>>> compact('SE 123456789701')
'123456789701'
>>> is_valid('123456789701')
True
>>> is_valid('123456789101')  # invalid check digits
False
"""

from stdnum import luhn
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('SE'):
        number = number[2:]
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return number.isdigit() and len(number) == 12 and \
           luhn.is_valid(number[:-2]) and 0 < int(number[-2:]) < 95
