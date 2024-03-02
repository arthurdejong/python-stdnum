# tan.py - functions for handling Mauritius TAN numbers
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

"""TAN (Tax Account Number, Mauritius tax number).

This number consists of 8 digits. For individuals the first digit is always 1,
5, 7 or 8. For entities the first digit is always 2 or 3.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Mauritius-TIN.pdf

>>> validate('20405553')
'20405553'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('20405553')
'20405553'
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
    """Check if the number is a valid Mauritius TAN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 8:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[0] not in ('1', '2', '3', '5', '7', '8'):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid Mauritius TAN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
