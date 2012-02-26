# cf.py - functions for handling Romanian CF (VAT) numbers
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

"""CF (Cod de înregistrare în scopuri de TVA, Romanian VAT number).

The Romanian CF is used for VAT purposes and can be from 2 to 10 digits long.

>>> compact('RO 185 472 90')
'18547290'
>>> is_valid('185 472 90')
True
>>> is_valid('185 472 91')  # invalid check digit
False
>>> is_valid('1630615123457')  # personal code
True
"""

from stdnum.ro import cnp
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('RO'):
        number = number[2:]
    return number


def calc_check_digit(number):
    """Calculate the check digit for organisations. The number passed
    should not have the check digit included."""
    weights = (7, 5, 3, 2, 1, 7, 5, 3, 2)
    number = (9 - len(number)) * '0' + number
    check = 10 * sum(weights[i] * int(n) for i, n in enumerate(number))
    return str(check % 11 % 10)


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if not number.isdigit() or number[0] == '0':
        return False
    if len(number) == 13:
        # apparently a CNP can also be used (however, not all sources agree)
        return cnp.is_valid(number)
    elif 2 <= len(number) <= 10:
        return calc_check_digit(number[:-1]) == number[-1]
    return False
