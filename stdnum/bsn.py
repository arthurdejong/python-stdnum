# bsn.py - functions for handling BSNs
#
# Copyright (C) 2010 Arthur de Jong
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

"""Module for handling BSNs (Burgerservicenummer), the
Dutch national identification number.

>>> validate('111222333')
True
>>> validate('111252333')
False
>>> compact('1234.56.782')
'123456782'
>>> format('111222333')
'1112.22.333'
"""


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = number.replace(' ','').replace('-','').replace('.','').strip()
    # padd with leading zeroes
    return (9 - len(number)) * '0' + number

def _calc_checksum(number):
    """Calculate the checksum over the number."""
    return sum( (9-i) * int(number[i]) for i in range(8) ) - int(number[8])

def validate(number):
    """Checks to see if the number provided is a valid BSN. This checks
    the length and whether the check digit is correct."""
    number = compact(number)
    return len(number) == 9 and \
           number.isdigit() and \
           int(number) > 0 and \
           _calc_checksum(number) % 11 == 0

def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return number[:4] + '.' + number[4:6] + '.' + number[6:]
