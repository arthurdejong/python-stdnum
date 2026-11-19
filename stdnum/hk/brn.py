# nit.py - functions for handling Hong Kong BR numbers
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

"""BRN (Bussiness Registration number, Hong Kong tax number).

Sometimes also called "商業登記號碼" or "BR No."

This number consists of 8 digits. It is the first 8 digits at the front of the
Business Registration Certificate Number, which in turn has the
22222222-XXX-XX-XX-X format. It is provided by the Inland Revenue Department
(IRD) of Hong Kong at the date of incorporation.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Hong-Kong-TIN.pdf
* https://sleek.com/hk/resources/hong-kong-business-registration-number-vs-company-registration-number/
* https://blog.startupr.hk/hong-kong-business-registration-number-brn/

>>> validate('31130878')
'31130878'
>>> validate('1767 4094')
'17674094'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('1767 4094')
'17674094'
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
    """Check if the number is a valid Hong Kong BR number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 8:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Hong Kong BR number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
