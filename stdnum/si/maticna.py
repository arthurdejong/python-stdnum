# maticna.py - functions for handling Slovenian Corporate Registration Numbers
# coding: utf-8
#
# Copyright (C) 2022 Blaž Bregar
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

"""Matična številka poslovnega registra (Corporate Registration Number)

The Corporate registration number represent a unique identification of
each unit of the business register, assigned by the registry administrator
at the time of entry in the business register, which shall not be changed.

The number consists of 10 digits and includes. First 6 digits represent a
unique number for each unit of company, followed by a check digit.
Last 3 digits represent an additional business unit of the company, starting
at 001. When a company consists of more than 1000 units, a letter is used
instead of the first digit in the business unit. Unit 000 always represents
the main registered address.

More information:

* http://www.pisrs.si/Pis.web/pregledPredpisa?id=URED7599

>>> validate('9331310000')
'9331310000'
>>> validate('9331320000')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').strip()
    if len(number) == 10 and number.endswith('000'):
        return number[0:7]
    return number


def calc_check_digit(number):
    """Calculate the check digit."""
    weights = (7, 6, 5, 4, 3, 2)
    total = sum(int(n) * w for n, w in zip(number[:6], weights))
    check = 11 - (total % 11)
    while check >= 10:
        check = check % 10
    return str(check)


def validate(number):
    """Check if the number is a valid Corporate Registration number. This
    checks the length and check digit."""
    number = clean(number)
    if not (len(number) == 7 or len(number) == 10):
        raise InvalidLength()
    if not isdigits(number[:6]):
        raise InvalidFormat()
    if calc_check_digit(number) != number[6]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if provided is valid ID. This checks the length,
    formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
