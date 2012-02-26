# vat.py - functions for handling Irish VAT numbers
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

"""VAT (Irish VAT number).

The Irish VAT number consists of 8 digits. The last digit is a check
letter, the second digit may be a number, a letter, "+" or "*".

>>> compact('IE 6433435F')
'6433435F'
>>> is_valid('6433435F')
True
>>> is_valid('6433435E')  # incorrect check digit
False
>>> is_valid('8D79739I')  # old style number
True
>>> is_valid('8?79739J')  # incorrect old style
False
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('IE'):
        number = number[2:]
    return number


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    alphabet = 'WABCDEFGHIJKLMNOPQRSTUV'
    number = (7 - len(number)) * '0' + number
    return alphabet[sum((8 - i) * int(n) for i, n in enumerate(number)) % 23]


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if len(number) != 8 or not number[0].isdigit() or \
       not number[2:7].isdigit():
         return False
    if number[:7].isdigit():
        # new system
        return number[-1] == calc_check_digit(number[:-1])
    if number[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ+*':
        # old system
        return number[-1] == calc_check_digit(number[2:-1] + number[0])
    return False
