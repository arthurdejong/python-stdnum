# nie.py - functions for handling Spanish foreigner identity codes
# coding: utf-8
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

"""NIE (Número de Identificación de Extranjeros, Spanish foreigner number).

The NIE is an identification number for foreigners. It is a 9 digit number
where the first digit is either X, Y or Z and last digit is a checksum
letter.

>>> compact('x-2482300w')
'X2482300W'
>>> is_valid('x-2482300w')
True
>>> is_valid('x-2482300a')  # invalid check digit
False
"""

from stdnum.es import dni


__all__ = ['compact', 'is_valid']


# use the same compact function as DNI
compact = dni.compact


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    # replace XYZ with 012
    number = str('XYZ'.index(number[0])) + number[1:]
    return dni.calc_check_digit(number)


def is_valid(number):
    """Checks to see if the number provided is a valid DNI number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 9 and number[1:-1].isdigit() and \
           number[0] in 'XYZ' and calc_check_digit(number[:-1]) == number[-1]
