# mod_97_10.py - functions for performing the ISO 7064 Mod 97, 10 algorithm
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

"""Module for calculation and verifying the check digits of a number
using the ISO 7064 Mod 97, 10 algorithm.

Validation can be done with is_valid(). A valid number can be made by
calculating the check digits and appending them.


>>> calc_check_digits('99991234567890121414')
'90'
>>> is_valid('9999123456789012141490')
True
>>> calc_check_digits('4354111611551114')
'31'
>>> is_valid('08686001256515001121751')
True
>>> calc_check_digits('22181321402534321446701611')
'35'
"""

def checksum(number):
    """Calculate the checksum."""
    return int(number) % 97

def calc_check_digits(number):
    """With the provided number, calculate the extra digit that should be
    appended to make it a valid number."""
    return '%02d' % (( 98 - 100 * checksum(number)) % 97)

def is_valid(number):
    """Determines whether the number has a valid checksum."""
    try:
        return bool(number) and checksum(number) == 1
    except:
        return False
