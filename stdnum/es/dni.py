# dni.py - functions for handling Spanish personal identity codes
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

"""DNI (Documento nacional de identidad, Spanish personal identity codes).

The DNI is a 9 digit number used to identify Spanish citizens. The last
digit is a checksum letter.

Foreign nationals, since 2010 are issued an NIE (Número de Identificación
de Extranjeros, Foreigner's Identity Number) instead.

>>> compact('54362315-K')
'54362315K'
>>> is_valid('54362315-K')
True
>>> is_valid('54362315Z')  # invalid check digit
False
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    return 'TRWAGMYFPDXBNJZSQVHLCKE'[int(number) % 23]


def is_valid(number):
    """Checks to see if the number provided is a valid DNI number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return number[:-1].isdigit() and len(number) == 9 and \
           calc_check_digit(number[:-1]) == number[-1]
