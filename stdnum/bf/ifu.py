# ifu.py - functions for handling Burkina Faso IFU numbers
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

"""IFU (Identifiant Financier Unique, Burkina Faso tax number).

This number consists of 9 characters, including a check character.

More information:

* https://www.impots.gov.bf/fileadmin/user_upload/storage/fichiers/Loi-058-portant-CODE-GENERAL-DES-IMPOTS-final.pdf
* http://dgi.impots.gov.bf/services-en-ligne/ifu/page4_7.php

>>> validate('00014729V')
'00014729V'
>>> validate('0000 59 83 T')
'00005983T'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('0000 59 83 T')
'00005983T'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -').upper().strip()


def validate(number):
    """Check if the number is a valid Burkina Faso IFU number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number[:-1]):
        raise InvalidFormat()
    if not number[-1].isalpha():
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Burkina Faso IFU number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)