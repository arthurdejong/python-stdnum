# verhoeff.py - functions for performing the Verhoeff checksum
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

"""The Verhoeff algorithm.

The Verhoeff algorithm uses two tables for permutations and
multiplications to calculate a checksum.

>>> is_valid('1234')
False
>>> checksum('1234')
1
>>> calc_check_digit('1234')
'0'
>>> is_valid('12340')
True
"""

# These are the multiplication and permutation tables used in the
# Verhoeff algorithm.

_multiplication_table = (
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0])

_permutation_table = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8))


def checksum(number):
    """Calculate the Verhoeff checksum over the provided number. The checksum
    is returned as an int. Valid numbers should have a checksum of 0."""
    # transform number list
    number = tuple(int(n) for n in reversed(str(number)))
    # calculate checksum
    check = 0
    for i, n in enumerate(number):
        check = _multiplication_table[check][_permutation_table[i % 8][n]]
    return check


def is_valid(number):
    """Checks to see if the number provided passes the Verhoeff checksum."""
    try:
        return bool(number) and checksum(number) == 0
    except:
        return False


def calc_check_digit(number):
    """With the provided number, calculate the extra digit that should be
    appended to make it pass the Verhoeff checksum."""
    return str(_multiplication_table[checksum(str(number) + '0')].index(0))
