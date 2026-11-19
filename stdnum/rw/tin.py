# tin.py - functions for handling Rwanda TIN numbers
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

"""TIN (Taxpayer's Identification Number, Rwanda tax number).

This number is also called "Numéro d'Identification du Contribuable", or
"Numéro d'identification fiscale" or "Nomero iranga umusoreshwa", and is also
shortened as "NIF".

This number consists of 9 digits.

More information:

* https://businessprocedures.rdb.rw/procedure/13/47?l=en
* https://www.rra.gov.rw/en/home

>>> validate('102134442')
'102134442'
>>> validate('10 7826151')
'107826151'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('10 7826151')
'107826151'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid Rwanda TIN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Rwanda TIN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
