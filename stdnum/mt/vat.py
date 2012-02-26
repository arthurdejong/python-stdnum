# vat.py - functions for handling Maltese VAT numbers
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

"""VAT (Maltese VAT number).

The Maltese VAT registration number contains 8 digits and uses a simple
weigted checksum.

>>> compact('MT 1167-9112')
'11679112'
>>> is_valid('1167-9112')
True
>>> is_valid('1167-9113')  # invalid check digits
False
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('MT'):
        number = number[2:]
    return number


def checksum(number):
    """Calculate the checksum."""
    weights = (3, 4, 6, 7, 8, 9, 10, 1)
    return sum(weights[i] * int(n) for i, n in enumerate(number)) % 37


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return number.isdigit() and len(number) == 8 and \
           number[0] != '0' and checksum(number) == 0
