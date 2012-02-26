# ismn.py - functions for handling ISMNs
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

"""ISMN (International Standard Music Number).

The ISMN (International Standard Music Number) is used to identify sheet
music. This module handles both numbers in the 10-digit 13-digit format.

>>> is_valid('979-0-3452-4680-5')
True
>>> is_valid('9790060115615')
True
>>> ismn_type(' M-2306-7118-7')
'ISMN10'
>>> is_valid('9790060115614') # incorrect check digit
False
>>> compact('  979-0-3452-4680-5')
'9790345246805'
>>> format('9790060115615')
'979-0-060-11561-5'
>>> format('M230671187')
'979-0-2306-7118-7'
>>> to_ismn13('M230671187')
'9790230671187'
"""

from stdnum import ean
from stdnum.util import clean


def compact(number):
    """Convert the ISMN to the minimal representation. This strips the number
    of any valid ISMN separators and removes surrounding whitespace."""
    return clean(number, ' -.').strip().upper()


def ismn_type(number):
    """Check the type of ISMN number passed and return 'ISMN13', 'ISMN10'
    or None (for invalid)."""
    try:
        number = compact(number)
    except:
        return None
    if len(number) == 10 and number[0] == 'M' and number[1:].isdigit():
        if ean.calc_check_digit('9790' + number[1:-1]) == number[-1]:
            return 'ISMN10'
    elif len(number) == 13 and number.isdigit():
        if ean.calc_check_digit(number[:-1]) == number[-1]:
            return 'ISMN13'
    return None


def is_valid(number):
    """Checks to see if the number provided is a valid ISMN (either a legacy
    10-digit one or a 13-digit one). This checks the length and the check
    bit but does not check if the publisher is known."""
    return ismn_type(number) is not None


def to_ismn13(number):
    """Convert the number to ISMN13 (EAN) format."""
    number = number.strip()
    min_number = compact(number)
    if len(min_number) == 13:
        return number  # nothing to do, already 13 digit format
    # add prefix and strip the M
    if ' ' in number:
        return '979 0' + number[1:]
    elif '-' in number:
        return '979-0' + number[1:]
    else:
        return '9790' + number[1:]


# these are the ranges allocated to publisher codes
_ranges = (
    (3, '000', '099'), (4, '1000', '3999'), (5, '40000', '69999'),
    (6, '700000', '899999'), (7, '9000000', '9999999'))


def split(number):
    """Split the specified ISMN into a bookland prefix (979), an ISMN
    prefix (0), a publisher element (3 to 7 digits), an item element (2 to
    6 digits) and a check digit."""
    # clean up number
    number = to_ismn13(compact(number))
    # rind the correct range and split the number
    for length, low, high in _ranges:
        if low <= number[4:4 + length] <= high:
            return (number[:3], number[3], number[4:4 + length],
                    number[4 + length:-1], number[-1])


def format(number, separator='-'):
    """Reformat the passed number to the standard format with the
    prefixes, the publisher element, the item element and the check-digit
    separated by the specified separator. The number is converted to the
    13-digit format silently."""
    return separator.join(x for x in split(number) if x)
