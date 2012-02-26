# pps.py - functions for handling Irish PPS numbers
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

"""PPS No (Personal Public Service Number, Irish personal number).

The Personal Public Service number consists of 8 digits. The first seven
are numeric and the last is the check character. The number is sometimes
be followed by an extra letter that can be a 'W', 'T' or an 'X' and is
ignored for the check algorithm.

>>> compact('6433435F')
'6433435F'
>>> is_valid('6433435F')
True
>>> is_valid('6433435E')  # incorrect check digit
False
"""

import re

from stdnum.util import clean
from stdnum.ie import vat


pps_re = re.compile('^\d{7}[A-W][WTX]?$')
"""Regular expression used to check syntax of PPS numbers."""


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def is_valid(number):
    """Checks to see if the number provided is a valid PPS number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if not pps_re.match(number):
        return False
    return number[7] == vat.calc_check_digit(number[:7])
