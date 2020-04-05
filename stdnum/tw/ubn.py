# ubn.py - functions for handling Taiwan UBN numbers
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

"""UBN (Unified Business Number or 統一編號, Taiwan tax number).

This number consists of 8 digits, the last being a check digit.

More information:

* https://zh.wikipedia.org/wiki/統一編號
* https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do?request_locale=en
* https://github.com/cakephp/localized/blob/d2216b50/src/Validation/TwValidation.php#L80-L101

>>> validate('00501503')
'00501503'
>>> validate('00501502')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format(' 0050150 3 ')
'00501503'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -').strip()


def calc_check_digit(number):
    """Calculate the check digit."""
    weights = (1, 2, 1, 2, 1, 2, 4, 1)
    sum_digits = lambda n: sum(int(c) for c in str(n))
    total = sum(sum_digits(int(character) * weight)
                for character, weight in zip(number, weights))
    remainder = total % 10
    if remainder == 0 or (remainder == 9 and number[6] == '7'):
        return number[-1]
    return None


def validate(number):
    """Check if the number is a valid Taiwan UBN number.

    This checks the length, formatting and check digit.
    """
    number = compact(number)
    if len(number) != 8:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if calc_check_digit(number) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid Taiwan UBN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
