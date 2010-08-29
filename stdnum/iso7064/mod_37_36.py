# mod_37_36.py - functions for performing the ISO 7064 Mod 37, 36 algorithm
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
using the ISO 7064 Mod 37, 36 algorithm.

Validation can be done with is_valid(). A valid number can be made by
calculating the check digit and appending it.

>>> checksum('A12425GABC1234002M')
1
>>> calc_check_digit('A12425GABC1234002')
'M'
>>> is_valid('A12425GABC1234002M')
True

By changing the alphabet this can be turned into any Mod x+1, x
algorithm. For example Mod 11, 10:

>>> calc_check_digit('00200667308', alphabet='0123456789')
'5'
>>> is_valid('002006673085', alphabet='0123456789')
True
"""


def checksum(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Calculate the checksum."""
    modulus = len(alphabet)
    check = modulus / 2
    for n in number:
        check = ( ((check or modulus) * 2) % (modulus + 1) + alphabet.index(n) ) % modulus
    return check

def calc_check_digit(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """With the provided number, calculate the extra digit that should be
    appended to make it a valid number."""
    modulus = len(alphabet)
    return alphabet[(1 - ( (checksum(number, alphabet) or modulus) * 2) % (modulus + 1) ) % modulus]

def is_valid(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Checks whether the check digit is valid."""
    try:
        return bool(number) and checksum(number, alphabet) == 1
    except:
        return False
