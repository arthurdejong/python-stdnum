# ifu.py - functions for handling Benin IFU numbers
# coding: utf-8
#
# Copyright (C) 2023 Leandro Regueiro
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

"""IFU (Identifiant Fiscal Unique, Benin tax number).

This number consists of 13 digits.

The first digit indicates the type of entity:
 * 1: Individual male
 * 2: Individual female
 * 3: Legal entity / company
 * 4: Legal person / state structure
 * 5: Legal person / international organization and mission diplomatic
 * 6: Legal person / non-governmental organization

The following four digits give the year. The next six digits are a unique
identifier within that year.

The next digit indicates either:

 * 1: a parent company
 * 2-9: subsidiary or agencies
 * 0: other types of person or taxpayer

The final digit is a check digit, which is used to verify the number was
correctly typed.

More information:

* http://www.finances.bj/sousSites/dgi/wp-content/uploads/2016/12/IFU.pdf

>>> validate('3201910583176')
'3201910583176'
>>> validate('3201 30109 9116')
'3201301099116'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('3201 30109 9116')
'3201301099116'
"""  # noqa: E501

from datetime import date

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid Benin IFU number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 13:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[0] not in ('1', '2', '3', '4', '5', '6'):
        raise InvalidComponent()
    if number[1:5] > date.today().strftime('%Y'):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid Benin IFU number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
