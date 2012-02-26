# pnf.py - functions for handling Bulgarian personal number of a foreigner
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

"""PNF (ЛНЧ, Личен номер на чужденец, Bulgarian number of a foreigner).

The personal number of a foreigner is a 10-digit number where the last digit
is the result of a weighted checksum.

>>> compact('7111 042 925')
'7111042925'
>>> is_valid('7111042925')
True
>>> is_valid('7111042922')  # invalid check digit
False
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -.').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    weights = (21, 19, 17, 13, 11, 9, 7, 3, 1)
    return str(sum(weights[i] * int(n) for i, n in enumerate(number)) % 10)


def is_valid(number):
    """Checks to see if the number provided is a valid national
    identification number. This checks the length, formatting, embedded
    date and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return number.isdigit() and len(number) == 10 and \
           calc_check_digit(number[:-1]) == number[-1]
