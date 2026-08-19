# bin.py - functions for handling Kazakhstan BIN numbers
# coding: utf-8
#
# Copyright (C) 2022 Leandro Regueiro
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

"""BIN or "БСН" (Business Identification Number, "бизнес-сәйкестендіру нөмірі",
Kazakhstan tax number).

This number consists of 12 digits and consists of five parts:

* First part: consists of 4 digits representing the year (the last two digits)
  and month of registration or re-registration.
* Second part: consists of 1 digit representing the type of legal entity or
  individual entrepreneur (C):
    4 - for resident legal entities;
    5 - for non-resident legal entities;
    6 - for IP (C).
* Third part: consists of 1 digit providing additional information:
    0 - head unit of a legal entity or individual entrepreneur (S);
    1 - branch of a legal entity or individual entrepreneur (S);
    2 - representation of a legal entity or individual entrepreneur (S);
    3 - a peasant (farm) farm operating on the basis of joint entrepreneurship.
* Fourth part: consists of 5 digits and is a serial number.
* Fifth part: consists of 1 check digit.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Kazakhstan-TIN.pdf

>>> validate('940140000385')
'940140000385'
>>> validate('990 140 004 654')
'990140004654'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('12345678901X')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('949940000385')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('940190000385')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('940149000385')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> format('990 140 004 654')
'990140004654'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' ')


def validate(number):
    """Check if the number is a valid Kazakhstan BIN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if int(number[2:4]) not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        raise InvalidComponent()
    if number[4] not in ('4', '5', '6'):
        raise InvalidComponent()
    if number[5] not in ('0', '1', '2', '3'):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid Kazakhstan BIN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
