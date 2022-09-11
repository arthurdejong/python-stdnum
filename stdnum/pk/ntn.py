# ntn.py - functions for handling Pakistan NTN numbers
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

"""NTN (National Tax Number, نیشنل ٹیکس نمبر, Pakistan tax number).

This number consists of 8 digits, the last being a check digit, usually
separated by a hyphen like XXXXXXX-X.

Companies and associations of persons (AOP) are assigned a National Tax Number
or Registration Number when they e-enroll on the FBR Iris portal.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Pakistan-TIN.pdf
* https://e.fbr.gov.pk/

>>> validate('3804142-1')
'38041421'
>>> validate('0822910 - 4')
'08229104'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('38041421')
'3804142-1'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -')


def validate(number):
    """Check if the number is a valid Pakistan NTN number.

    This checks the length, formatting and check digit.
    """
    number = compact(number)
    if len(number) != 8:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Pakistan NTN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join([number[:-1], number[-1]])
