# rocbn.py - functions for handling Brunei ROCBN numbers
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

"""ROCBN (Brunei tax number).

This number consists of 8 digits, prepended by the letter 'P' for
Sole-Proprietorships or Partnerships, or by the letters 'RC' for Private
Limited Companies and Public Companies, or by the letters 'RFC' for Foreign
Branch of companies.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Brunei-darussalam-TIN%20.pdf

>>> validate('RC00004866')
'RC00004866'
>>> validate('RFC/00000772')
'RFC00000772'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('RFC/00000772')
'RFC00000772'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -/').upper().strip()


def validate(number):
    """Check if the number is a valid Brunei ROCBN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) not in (9, 10, 11):
        raise InvalidLength()
    if not isdigits(number[-8:]):
        raise InvalidFormat()
    if len(number) == 9 and not number.startswith('P'):
        raise InvalidFormat()
    if len(number) == 10 and not number.startswith('RC'):
        raise InvalidFormat()
    if len(number) == 11 and not number.startswith('RFC'):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Brunei ROCBN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
