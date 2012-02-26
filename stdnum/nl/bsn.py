# bsn.py - functions for handling BSNs
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

"""BSN (Burgerservicenummer, the Dutch national identification number).

The BSN is a number with up to 9 digits (the leading 0's are commonly left
out) which is used as the Dutch national identification number.

>>> is_valid('111222333')
True
>>> is_valid('111252333')
False
>>> compact('1234.56.782')
'123456782'
>>> format('111222333')
'1112.22.333'
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').strip()
    # pad with leading zeroes
    return (9 - len(number)) * '0' + number


def checksum(number):
    """Calculate the checksum over the number. A valid number should have
    a check digit of 0."""
    return (sum((9 - i) * int(n) for i, n in enumerate(number[:-1])) -
            int(number[-1])) % 11


def is_valid(number):
    """Checks to see if the number provided is a valid BSN. This checks
    the length and whether the check digit is correct."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 9 and number.isdigit() and \
           int(number) > 0 and checksum(number) == 0


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return number[:4] + '.' + number[4:6] + '.' + number[6:]
