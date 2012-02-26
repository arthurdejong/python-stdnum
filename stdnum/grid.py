# grid.py - functions for handling Global Release Identifier (GRid) numbers
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

"""GRid (Global Release Identifier).

The Global Release Identifier is used to identify releases of digital
sound recordings and uses the ISO 7064 Mod 37, 36 algorithm to verify the
correctness of the number.

>>> is_valid('A12425GABC1234002M')
True
>>> is_valid('Grid: A1-2425G-ABC1234002-M')
True
>>> is_valid('A1-2425G-ABC1234002-Q') # incorrect check digit
False
>>> is_valid(None) # method should be robust
False
>>> compact('A1-2425G-ABC1234002-M')
'A12425GABC1234002M'
>>> format('A12425GABC1234002M')
'A1-2425G-ABC1234002-M'
"""

from stdnum.util import clean


def compact(number):
    """Convert the GRid to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').strip().upper()
    if number.startswith('GRID:'):
        number = number[5:]
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid GRid."""
    from stdnum.iso7064 import mod_37_36
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 18 and mod_37_36.is_valid(number)


def format(number, separator='-', add_check_digit=False):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    number = (number[0:2], number[2:7], number[7:17], number[17:])
    return separator.join(x for x in number if x)
