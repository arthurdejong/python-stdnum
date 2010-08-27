# mod_11_10.py - functions for performing the ISO 7064 Mod 11, 10 algorithm
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

"""Module for calculation and verifying the checksum of a number
using the ISO 7064 Mod 11, 10 algorithm.

Validation can be done with is_valid(). A valid number can be made by
calculating the check digit and appending it.

>>> calc_check_digit('79462')
'3'
>>> is_valid('794623')
True
>>> calc_check_digit('00200667308')
'5'
>>> is_valid('002006673085')
True
"""


def checksum(number):
    """Calculate the checksum."""
    check = 5
    for n in number:
        check = ( ((check or 10) * 2) % 11 + int(n) ) % 10
    return check

def calc_check_digit(number):
    """With the provided number, calculate the extra digit that should be
    appended to make it a valid number."""
    return str((1 - ( (checksum(number) or 10) * 2) % 11 ) % 10)

def is_valid(number):
    """Checks whether the check digit is valid."""
    try:
        return bool(number) and checksum(number) == 1
    except:
        return False
