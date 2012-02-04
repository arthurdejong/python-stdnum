# btw.py - functions for handling Dutch VAT numbers
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

"""Module for handling Dutch VAT (BTW) numbers.

>>> is_valid('00449544B01')
True
>>> is_valid('NL449544B01')
True
>>> is_valid('123456789B90')
False
"""

from stdnum.nl import bsn
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('NL'):
        number = number[2:]
    return bsn.compact(number[:-3]) + number[-3:]


def is_valid(number):
    """Checks to see if the number provided is a valid BTW number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 12 and \
           number[9] == 'B' and \
           number[10:].isdigit() and \
           bsn.is_valid(number[0:9])
