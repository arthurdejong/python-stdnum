# cif.py - functions for handling Spanish fiscal numbers
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

"""CIF (Certificado de Identificación Fiscal, Spanish company tax number).

The CIF is a tax identification number for legal entities. It has 9 digits
where the first digit is a letter (denoting the type of entity) and the
last is a check digit (which may also be a letter).

>>> compact('J-99216582')
'J99216582'
>>> is_valid('J99216582')
True
>>> is_valid('J99216583')  # invalid check digit
False
>>> is_valid('M-1234567-L')
True
>>> is_valid('O-1234567-L')  # invalid first character
False
>>> split('A13 585 625')
('A', '13', '58562', '5')
"""

from stdnum import luhn
from stdnum.es import dni


__all__ = ['compact', 'is_valid', 'split']


# use the same compact function as DNI
compact = dni.compact


def calc_check_digits(number):
    """Calculate the check digits for the specified number. The number
    passed should not have the check digit included. This function returns
    both the number and character check digit candidates."""
    check = luhn.calc_check_digit(number[1:])
    return check + 'JABCDEFGHI'[int(check)]


def is_valid(number):
    """Checks to see if the number provided is a valid DNI number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if len(number) != 9 or not number[1:-1].isdigit():
        return False
    if number[0] in 'KLM':
        # K: Spanish younger than 14 year old
        # L: Spanish living outside Spain without DNI
        # M: granted the tax to foreigners who have no NIE
        # these use the old checkdigit algorithm (the DNI one)
        return number[-1] == dni.calc_check_digit(number[1:-1])
    # there seems to be conflicting information on which organisation types
    # should have which type of check digit (alphabetic or numeric) so
    # we support either here
    if number[0] in 'ABCDEFGHJNPQRSUVW':
        return number[-1] in calc_check_digits(number[:-1])
    # anything else is invalid
    return False


def split(number):
    """Split the provided number into a letter to define the type of
    organisation, two digits that specify a province, a 5 digit sequence
    number within the province and a check digit."""
    number = compact(number)
    return number[0], number[1:3], number[3:8], number[8:]
