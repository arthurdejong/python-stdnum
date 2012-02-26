# mod_37_2.py - functions for performing the ISO 7064 Mod 37, 2 algorithm
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

"""The ISO 7064 Mod 37, 2 algorithm.

The Mod 37, 2 checksum can be used for alphanumeric numbers and the check
digit may also be numeric, a letter or '*'.

>>> calc_check_digit('G123489654321')
'Y'
>>> is_valid('G123489654321Y')
True
>>> checksum('G123489654321Y')
1

By changing the alphabet this can be turned into any Mod x, 2
algorithm. For example Mod 11, 2:

>>> calc_check_digit('079', alphabet='0123456789X')
'X'
>>> is_valid('079', alphabet='0123456789X')
True
>>> checksum('079', alphabet='0123456789X')
1
"""


def checksum(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*'):
    """Calculate the checksum. A valid number should have a checksum of 1."""
    modulus = len(alphabet)
    check = 0
    for n in number:
        check = (2 * check + alphabet.index(n)) % modulus
    return check


def calc_check_digit(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*'):
    """With the provided number, calculate the extra digit that should be
    appended to make it a valid number."""
    modulus = len(alphabet)
    return alphabet[(1 - 2 * checksum(number, alphabet)) % modulus]


def is_valid(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ*'):
    """Checks whether the check digit is valid."""
    try:
        return bool(number) and checksum(number, alphabet) == 1
    except:
        return False
