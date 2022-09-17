# voen.py - functions for handling Azerbaijan VOEN numbers
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

"""VÖEN (Vergi ödəyicisinin eyniləşdirmə nömrəsi, Azerbaijan tax number).

This number consists of 10 digits.

The first two digits are the code for the territorial administrative unit. The
following six digits are a serial number. The ninth digit is determined by some
special algorithm. The tenth digit represents the legal status of a taxpayer:
1 for legal persons and 2 for natural persons.


More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Azerbaijan-TIN.pdf
* https://www.e-taxes.gov.az/ebyn/payerOrVoenChecker.jsp

>>> validate('1400057421')
'1400057421'
>>> validate('140 155 5071')
'1401555071'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('1400057424')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> format('140 155 5071')
'1401555071'
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
    """Check if the number is a valid Azerbaijan VÖEN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[-1] not in ('1', '2'):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid Azerbaijan VÖEN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
