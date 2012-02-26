# ean.py - functions for handling EANs
#
# Copyright (C) 2011, 2012 Arthur de Jong
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

"""EAN (International Article Number).

Module for handling EAN (International Article Number) codes. This
module handles numbers EAN-13, EAN-8 and UPC (12-digit) format.

>>> is_valid('73513537')
True
>>> is_valid('978-0-471-11709-4') # ISBN-13 format
True
"""

from stdnum.util import clean


def compact(number):
    """Convert the EAN to the minimal representation. This strips the number
    of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def calc_check_digit(number):
    """Calculate the EAN check digit for 13-digit numbers. The number passed
    should not have the check bit included."""
    return str((10 - sum((3 - 2 * (i % 2)) * int(n)
                         for i, n in enumerate(reversed(number)))) % 10)


def is_valid(number):
    """Checks to see if the number provided is a valid EAN-13. This checks
    the length and the check bit but does not check whether a known GS1
    Prefix and company identifier are referenced."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) in (13, 12, 8) and \
           number.isdigit() and \
           calc_check_digit(number[:-1]) == number[-1]
