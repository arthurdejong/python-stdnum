# cpr.py - functions for handling Danish CPR numbers
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

"""CPR (personnummer, the Danish citizen number).

The CPR is the national number to identify Danish citizens. The number
consists of 10 digits in the format DDMMYY-SSSS where the first part
represents the birth date and the second a sequence number. The first
digit of the sequence number indicates the century.

The numbers used to validate using a checksum but since the sequence
numbers ran out this was abandoned in 2007.

>>> compact('211062-5629')
'2110625629'
>>> is_valid('211062-5629')
True
>>> checksum('2110625629')
0
>>> is_valid('511062-5629')  # invalid date
False
>>> get_birth_date('2110620629')
datetime.date(1962, 10, 21)
>>> get_birth_date('2110525629')
datetime.date(2052, 10, 21)
>>> format('2110625629')
'211062-5629'
"""

import datetime

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def checksum(number):
    """Calculate the checksum. Note that the checksum isn't actually used
    any more. Valid numbers used to have a checksum of 0."""
    weights = (4, 3, 2, 7, 6, 5, 4, 3, 2, 1)
    return sum(weights[i] * int(n) for i, n in enumerate(number)) % 11


def get_birth_date(number):
    """Split the date parts from the number and return the birth date."""
    day = int(number[0:2])
    month = int(number[2:4])
    year = int(number[4:6])
    if number[6] in '5678' and year >= 58:
        year += 1800
    elif number[6] in '0123' or (number[6] in '49' and year >= 37):
        year += 1900
    else:
        year += 2000
    return datetime.date(year, month, day)


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if not number.isdigit() or len(number) != 10:
        return False
    # check if birth date is valid
    try:
        birth_date = get_birth_date(number)
        # TODO: check that the birth date is not in the future
    except ValueError, e:
        return False
    return True


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return '-'.join((number[:6], number[6:]))
