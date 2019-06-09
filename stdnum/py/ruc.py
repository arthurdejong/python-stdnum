# rut.py - functions for handling Paraguay RUC numbers
# coding: utf-8
#
# Copyright (C) 2019 Leandro Regueiro
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

"""RUC number (Paraguay Registro Único de Contribuyentes number).

The RUC number for juridical persons consists of 8 digits starting after
80000000, followed by a check digit. For physical persons consists of an
undetermined number of digits followed by a check digit.

Online search: https://www.ruc.com.py/

>>> validate('80028061-0')
'800280610'
>>> validate('PY 80006952-8')
'800069528'
>>> validate('9991603')
'9991603'
>>> validate('2660-3')
'26603'
>>> validate('800532492')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('80123456789')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('800000358')
'80000035-8'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


WEIGHTS = [9, 8, 7, 6, 5, 4, 3, 2]


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    number = clean(number, ' -').upper().strip()

    if number.startswith('PY'):
        return number[2:]

    return number


def calc_check_digit(number):
    """Calculate the check digit.

    The number passed should not have the check digit included.
    """
    # Pad number with zeroes on the left up to 8 digits if necessary.
    number = '0' * (8 - len(number)) + number

    total = sum(int(digit) * weight for digit, weight in zip(number, WEIGHTS))

    return str(-total % 11)[-1]  # If check digit is '10' return '0'.


def validate(number):
    """Check if the number is a valid Paraguay RUC number.

    This checks the length, formatting and check digit.
    """
    number = compact(number)

    if len(number) > 9:
        raise InvalidLength()

    if not isdigits(number):
        raise InvalidFormat()

    if number[-1] != calc_check_digit(number[:-1]):
        raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number is a valid Paraguay RUC number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join([number[:-1], number[-1]])
