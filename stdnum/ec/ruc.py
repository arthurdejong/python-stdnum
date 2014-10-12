# cif.py - functions for handling Ecuadorian fiscal numbers
# coding: utf-8
#
# Copyright (C) 2014 Jonathan Finlay
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

"""RUC (Registro Único de Contribuyentes, Ecuadorian company tax number).

The RUC is a tax identification number for legal entities. It has 13 digits
where the third digit is a number who denoting the type of entity.

>>> validate('1714307103001') # Natural entity
'1714307103001'
>>> validate('1768152130001') # Public entity
'1763154690001'
>>> validate('1792060346001') # Juridical entity
'1792060346001'
>>> validate('1792060346-001')
'1763154690001'
>>> validate('1763154690001')  # Invalid
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('179206034601')  # too short
Traceback (most recent call last):
    ...
InvalidLength: ...
"""

from stdnum.ec import ci
from stdnum.exceptions import *


__all__ = ['compact', 'validate', 'is_valid']


# use the same compact function as CI
compact = ci.compact

def calc_check_sum(number):
    result = 0
    if int(number[2]) == 6:
        # 6 = Public RUC
        coefficient = "32765432"
        result = sum(int(number[i]) * int(coefficient[i]) for i in range(8))
        residue = result % 11
        if residue == 0:
            result = residue
        else:
            result = 11 - residue
    elif int(number[2]) == 9:
        # 9 = Juridical RUC
        coefficient = "432765432"
        result = sum(int(number[i]) * int(coefficient[i]) for i in range(9))
        residue = result % 11
        if residue == 0:
            result = residue
        else:
            result = 11 - residue
    elif int(number[2]) < 6:
        # less than 6 = Natural RUC
        coefficient = "212121212"
        for i in range(9):
            suma = int(number[i]) * int(coefficient[i])
            if suma > 10:
                str_sum = str(suma)
                suma = int(str_sum[0]) + int(str_sum[1])
            result += suma
        residue = result % 10
        if residue == 0:
            result = residue
        else:
            result = 10 - residue
    else:
        raise InvalidFormat()
    return result


def validate(number):
    """Checks to see if the number provided is a valid RUC number. This
    checks the length, formatting, check digit and check sum."""
    number = compact(number)
    if len(number) != 13:
        raise InvalidLength()
    if not number.isdigit():
        raise InvalidFormat()
    checker = int(number[8]) if int(number[2]) == 6 else int(number[9])
    if calc_check_sum(number) != checker:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid RUC number. This
    checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
