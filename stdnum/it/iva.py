# vat.py - functions for handling Italian VAT numbers
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

"""Module for handling Italian IVA (Partita IVA (Imposta sul valore
aggiunto), VAT) numbers.

The number consists of 11 digits. The first 7 digits are a company
identifier, tge next 3 refer to the province of residence and the last is
a check digit.

Note that the fiscal code for individuals is not accepted as valid code
for intracommunity VAT related operations so it is ignored here.

>>> compact('IT 00743110157')
'00743110157'
>>> is_valid('00743110157')
True
>>> is_valid('00743110158')  # invalid check digit
False
"""

from stdnum.util import clean, digitsum


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    if number.startswith('IT'):
        number = number[2:]
    return number


def checksum(number):
    """Calculate the checksum."""
    return digitsum(
            (1 + (i % 2)) * int(n)
            for i, n in enumerate(number)) % 10


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 11 and number.isdigit() and \
           int(number[0:7]) > 0 and (
              '001' <= number[7:10] <= '100' or
              number[7:10] in ('120', '121', '888', '999')
           ) and checksum(number) == 0
