# egn.py - functions for handling Bulgarian national identification numbers
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

"""EGN (ЕГН, Единен граждански номер, Bulgarian personal identity codes).

It is a 10-digit number of which the first 6 digits denote the person's
birth date, the next three digits represent a birth order number from
which the person's gender can be determined and the last digit is a check
digit.

>>> compact('752316 926 3')
'7523169263'
>>> is_valid('8032056031')
True
>>> get_birth_date('7542011030')
datetime.date(2075, 2, 1)
>>> is_valid('7552010004')  # invalid check digit
False
>>> is_valid('8019010008')  # invalid date
False
"""

import datetime

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -.').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    weights = (2, 4, 8, 5, 10, 9, 7, 3, 6)
    return str(sum(weights[i] * int(n) for i, n in enumerate(number)) % 11 % 10)


def get_birth_date(number):
    """Split the date parts from the number and return the birth date."""
    year = int(number[0:2]) + 1900
    month = int(number[2:4])
    day = int(number[4:6])
    if month > 40:
        year += 100
        month -= 40
    elif month > 20:
        year -= 100
        month -= 20
    return datetime.date(year, month, day)


def is_valid(number):
    """Checks to see if the number provided is a valid national
    identification number. This checks the length, formatting, embedded
    date and check digit."""
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
    # check the check digit
    return calc_check_digit(number[:-1]) == number[-1]
