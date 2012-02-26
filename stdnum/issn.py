# issn.py - functions for handling ISSNs
#
# Copyright (C) 2010, 2011, 2012 Arthur de Jong
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

"""ISSN (International Standard Serial Number).

The ISSN (International Standard Serial Number) is the standard code to
identify periodical publications. It has a checksum similar to ISBN-10.

>>> is_valid('0024-9319')
True
>>> is_valid('0032147X') # incorrect check digit
False
>>> compact('0032-1478')
'00321478'
>>> format('00249319')
'0024-9319'
>>> to_ean('0264-3596')
'9770264359008'
"""

from stdnum import ean
from stdnum.util import clean


def compact(number):
    """Convert the ISSN to the minimal representation. This strips the number
    of any valid ISSN separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def calc_check_digit(number):
    """Calculate the ISSN check digit for 10-digit numbers. The number passed
    should not have the check bit included."""
    check = (11 - sum((8 - i) * int(n)
                      for i, n in enumerate(number))) % 11
    return 'X' if check == 10 else str(check)


def is_valid(number):
    """Checks to see if the number provided is a valid ISSN. This checks
    the length and whether the check digit is correct."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 8 and \
           number[:-1].isdigit() and \
           calc_check_digit(number[:-1]) == number[-1]


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return number[:4] + '-' + number[4:]


def to_ean(number, issue_code='00'):
    """Convert the number to EAN-13 format. The number is assumed to be a
    valid ISSN."""
    number = '977' + compact(number)[:-1] + issue_code
    return number + ean.calc_check_digit(number)
