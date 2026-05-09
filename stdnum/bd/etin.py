# etin.py - functions for handling Bangladesh e-TIN numbers
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

"""e-TIN (Electronic Taxpayer's Identification Number, Bangladesh tax number).

This number consists of 12 digits.

More information:

* http://bdlaws.minlaw.gov.bd/act-672/section-34615.html
* https://www.incometax.gov.bd/TINHome
* https://royandassociates.com.bd/how-to-register-for-e-tin-certificate-in-bangladesh/
* https://tin-check.com/en/bangladesh/

>>> validate('224187378587')
'224187378587'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('224187378587')
'224187378587'
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
    """Check if the number is a valid Bangladesh e-TIN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 12:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Bangladesh e-TIN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
