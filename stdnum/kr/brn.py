# brn.py - functions for handling South Korea BRN numbers
# coding: utf-8
#
# Copyright (C) 2020 Leandro Regueiro
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

"""BRN (사업자 등록 번호, South Korea Business Registration Number).

The Business Registration Number consists of 10 digits.

The first three digits are serially assigned a three digit number
between 101 and 999.

The next two digits distinguish between an individual and a corporation
and are assigned based on the following criteria:

  01-79: sole proprietor liable for value-added tax (VAT).
  90-99: sole proprietor exempted from value-added tax (VAT).
  89: non-corporate religious organization.
  80: non-corporate organization excluding religious group (89).
  81, 86, 87, 88: head office of a for-profit corporation.
  82: head or branch office of a nonprofit corporation.
  83: country, local government or local government association.
  84: head, branch or liaison office of a foreign corporation.
  85: branch office of a for-profit corporation.

The next four digits are serially assigned between 0001-9999.

The last digit is a check digit that checks for any errors entered in
the first nine digits.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Korea-TIN.pdf

>>> validate('116-82-00276')
'1168200276'
>>> validate('1168200276')
'1168200276'
>>> validate(' 116 - 82 - 00276  ')
'1168200276'
>>> validate('123456789')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('1348672683')
'134-86-72683'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -').strip()


def validate(number):
    """Check if the number is a valid South Korea BRN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[:3] < '101':
        raise InvalidComponent()
    if number[5:-1] == '0000':
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid South Korea BRN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join([number[:3], number[3:5], number[5:]])
