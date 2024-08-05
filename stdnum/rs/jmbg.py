# jmbg.py - functions for handling Serbian JMBG (unique personal identification) numbers
# coding: utf-8
#
# Copyright (C) 2017 Arthur de Jong
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

"""JMBG (Jedinstveni Matični Broj Građana, Serbian unique citizen identification number).

The Serbian unique citizen identification number consists of 13 digits where the last
digit is a check digit.

>>> validate('0101900350008')
'0101900350008'
>>> validate('0101900350007')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.exceptions import *
from stdnum import luhn
from datetime import datetime
from stdnum.util import clean, isdigits
import re

REGEX = r"(\d{2})(\d{2})(\d{3})(\d{2})(\d{3})(\d{1})"

def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any blank spaces and removes surrounding whitespace."""
    return clean(number, ' ').strip()


def validate(number):
    """Check if the number is a valid JMBG number. This checks the length,
    formatting and check digit. """
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()

    day, month, year, region, sex, control = split_fields(number)
    human_year =  int(f"1{year}")

    if verify_date(day, month, human_year):
        number_sum = get_sum(number)
        if verify_control(number_sum, control) == False:
            raise InvalidChecksum()

    return number

def get_sum(number):
    first = number[0:6]
    second = number[6:-1]
    multiplier = [7, 6, 5, 4, 3, 2]

    first_sum = sum([int(a) * b for a, b in zip(first, multiplier)])
    second_sum = sum([int(a) * b for a, b in zip(second, multiplier)])

    return first_sum + second_sum

def verify_date(day, month, year):
    try:
        if isinstance(day, str):
            day = int(day)

        if isinstance(month, str):
            month = int(month)

        datetime(year, month, day)

        return True

    except Exception:
        raise InvalidFormat()

def verify_control(number_sum, control):
    control = int(control)
    remainder = number_sum % 11

    if remainder > 1:
        return control == 11 - remainder

    elif remainder == 0 and remainder == control:
        return True

    return False

def split_fields(jmbg):
    match = re.match(REGEX, jmbg)

    if not match:
        raise InvalidFormat()

    return match.groups()

def is_valid(number):
    """Check if the number is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
