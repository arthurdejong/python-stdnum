# vat.py - functions for handling Slovak VAT numbers
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

"""IČ DPH (IČ pre daň z pridanej hodnoty, Slovak VAT number).

The IČ DPH (Identifikačné číslo pre daň z pridanej hodnoty) is a 10-digit
number used for VAT purposes. It has a straightforward checksum.

>>> compact('SK 202 274 96 19')
'2022749619'
>>> is_valid('SK 202 274 96 19')
True
>>> is_valid('SK 202 274 96 18')  # invalid check digits
False
"""

from stdnum.sk import rc
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('SK'):
        number = number[2:]
    return number


def checksum(number):
    """Calculate the checksum."""
    return int(number) % 11


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if not number.isdigit() or len(number) != 10:
        return False
    # it is unclear whether the RČ can be used as a valid VAT number
    return rc.is_valid(number) or \
           (number[0] != '0' and int(number[2]) in (2, 3, 4, 7, 8, 9) and
            checksum(number) == 0)
