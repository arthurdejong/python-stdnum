# cnp.py - functions for handling Romanian CNP numbers
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

"""CNP (Cod Numeric Personal, Romanian Numerical Personal Code).

The CNP is a 13 digit number that includes information on the person's
gender, birth date and country zone.

>>> compact('1630615123457')
'1630615123457'
>>> is_valid('1630615123457')
True
>>> is_valid('8800101221144')  # invalid first digit
False
>>> is_valid('1632215123457')  # invalid date
False
>>> is_valid('1630615123458')  # invalid check digit
False
"""

import datetime

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit for personal codes. The number passed
    should not have the check digit included."""
    # note that this algorithm has not been confirmed by an independent source
    weights = (2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9)
    check = sum(weights[i] * int(n) for i, n in enumerate(number)) % 11
    return '1' if check == 10 else str(check)


def get_birth_date(number):
    """Split the date parts from the number and return the birth date."""
    centuries = {
        '1': 1900, '2': 1900, '3': 1800, '4': 1800, '5': 2000, '6': 2000,
    }  # we assume 1900 for the others in order to try to construct a date
    year = int(number[1:3]) + centuries.get(number[0], 1900)
    month = int(number[3:5])
    day = int(number[5:7])
    return datetime.date(year, month, day)


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if len(number) != 13 or not number.isdigit():
        return False
    # first digit should be a known one (9=foreigner)
    if number[0] not in '1234569':
        return False
    # check if birth date is valid
    try:
        birth_date = get_birth_date(number)
        # TODO: check that the birth date is not in the future
    except ValueError, e:
        return False
    # number[7:9] is the county, we ignore it for now, just check last digit
    return calc_check_digit(number[:-1]) == number[-1]
