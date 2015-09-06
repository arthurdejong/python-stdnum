# pesel.py - functions for handling REGON numbers
# coding: utf-8
#
# Copyright (C) 2015 Dariusz Choruzy
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

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def checksum(number):
    """Calculate the checksum."""
    if len(number) == 9:
        weights = (8, 9, 2, 3, 4, 5, 6, 7)
    else:
        weights = (2, 4, 8, 5, 0, 9, 7, 3, 6, 1, 2, 4, 8)
    return sum(weights[i] * int(n) for i, n in enumerate(number[:-1])) % 11


def validate(number):
    """Checks to see if the number provided is a valid REGON number. This
    checks the length, formatting and check digit."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) not in (9, 14):
        raise InvalidLength()
    sum_c = checksum(number)
    sum_c = 0 if sum_c == 10 else sum_c
    if str(sum_c) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid REGON number. This
    checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
