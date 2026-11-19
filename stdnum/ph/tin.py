# tin.py - functions for handling Philippines TIN numbers
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

"""TIN (Taxpayer Identification Number, Philippines tax number).

This number consists of 9 digits (for individual taxpayers), or 12 digits (for
bussinesses). A thirteenth digit will be added in the future for businesses).
It is usually separated using hyphens to make it easier to read, like
XXX-XXX-XXX-XXX.

The first digit identifies the type of taxpayer: 0 for businesses and 1 to 9
for individual taxpayers. The following seven digits are a sequence. The ninth
digit is the check digit.

The last three digits (four in the future), for businesses only, correspond to
the branch code. If the branch code is not specified, then it defaults to 000.

It is not specified in the official documents, but it is not uncommon that some
letters are appended to the businesses TIN to tell whether it is subject to
VAT, usually N to say it is not subject and V to tell that it is.

More information:

* https://www.ntrc.gov.ph/images/journal/j20141112a.pdf
* https://wiki.scn.sap.com/wiki/display/CRM/Philippines
* https://help.sap.com/doc/saphelp_erp2005/6.0/ja-JP/d8/663e399265df0ee10000000a11402f/content.htm
* https://world.salestaxhandbook.com/ph-philippines

>>> validate('239-072-842')
'239072842'
>>> validate('239-072-842-000')
'239072842000'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('12345678X')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> format('239072842000')
'239-072-842-000'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    number = clean(number, ' -').upper().strip()
    # Normalize unofficial code telling whether it is subject or not to VAT.
    number = number.replace('NONVAT', 'N')
    number = number.replace('NVAT', 'N')
    number = number.replace('NV', 'N')
    number = number.replace('VAT', 'V')
    # Append the default branch code for business TIN numbers having unofficial
    # VAT letter.
    if len(number) == 10 and number[-1] in ('N', 'V'):
        number = number[:-1] + '000' + number[-1]
    return number


def validate(number):
    """Check if the number is a valid Philippines TIN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) not in (9, 12, 13, 14):
        raise InvalidLength()
    has_wrong_format = not (isdigits(number) or
                            (number[-1] in ('N', 'V') and
                             isdigits(number[:-1])))
    if has_wrong_format:
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Philippines TIN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    if len(number) < 12:
        return '-'.join([number[:3], number[3:6], number[6:]])
    return '-'.join([number[:3], number[3:6], number[6:9], number[9:]])
