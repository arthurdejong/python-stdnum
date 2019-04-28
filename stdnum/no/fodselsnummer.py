# fodselsnummer.py - functions for handling Norwegian birth numbers
# coding: utf-8
#
# Copyright (C) 2018 Ilya Vihtinsky
# Copyright (C) 2018 Arthur de Jong
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

"""Fødselsnummer (Norwegian birth number, the national identity number).

The Fødselsnummer is an eleven-digit number that is built up of the date of
birth of the person, a serial number and two check digits.

More information:

* https://no.wikipedia.org/wiki/F%C3%B8dselsnummer
* https://en.wikipedia.org/wiki/National_identification_number#Norway

>>> validate('684131 52112')
'68413152112'
>>> get_gender('684131 52112')
'M'
>>> validate('684131 52123')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('68413152112')
'684131 52112'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -:')


def calc_check_digit1(number):
    """Calculate the first check digit for the number."""
    weights = (3, 7, 6, 1, 8, 9, 4, 5, 2)
    return str((11 - sum(w * int(n) for w, n in zip(weights, number))) % 11)


def calc_check_digit2(number):
    """Calculate the second check digit for the number."""
    weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
    return str((11 - sum(w * int(n) for w, n in zip(weights, number))) % 11)


def get_gender(number):
    """Get the person's birth gender ('M' or 'F')."""
    number = compact(number)
    if int(number[8]) % 2:
        return 'M'
    else:
        return 'F'


def validate(number):
    """Check if the number is a valid birth number."""
    number = compact(number)
    if len(number) != 11:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[-2] != calc_check_digit1(number):
        raise InvalidChecksum()
    if number[-1] != calc_check_digit2(number):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid birth number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return number[:6] + ' ' + number[6:]
