# ird.py - functions for handling New Zealand IRD numbers
# coding: utf-8
#
# Copyright (C) 2019 Leandro Regueiro
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

"""IRD number (New Zealand Inland Revenue Department (Te Tari Tāke) number).

The IRD number consists of 7 or 8 digits, followed by a check digit.

https://www.ird.govt.nz/-/media/Project/IR/PDF/2020RWTNRWTSpecificationDocumentv10.pdf

https://www.ird.govt.nz/resources/9/e/9e408a004e329f16a91bbf8ad6853786/rwt-nrwt-spec-2013+v1.0+.pdf

https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/New%20Zealand-TIN.pdf

>>> validate('4909185-0')
'49091850'
>>> validate('NZ 49-098-576')
'49098576'
>>> validate('136410133')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('9125568')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('49098576')
'49-098-576'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


PRIMARY_WEIGHTS = [3, 2, 7, 6, 5, 4, 3, 2]
SECONDARY_WEIGHTS = [7, 4, 3, 2, 5, 2, 7, 6]


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    number = clean(number, ' -').upper().strip()

    if number.startswith('NZ'):
        return number[2:]

    return number


def calc_check_digit(number):
    """Calculate the check digit.

    The number passed should not have the check digit included.
    """
    # Helper function to calculate the IRD verification digit.
    def _calculate_digit(weights):
        total = sum(int(digit) * weight
                    for digit, weight in zip(number, weights))
        return -total % 11

    # Add padding zero if necessary.
    if len(number) == 7:
        number = '0' + number

    # Calculate the verification digit.
    check_digit = _calculate_digit(PRIMARY_WEIGHTS)

    if check_digit != 10:
        return str(check_digit)

    # A second calculation is necessary.
    return str(_calculate_digit(SECONDARY_WEIGHTS))


def validate(number):
    """Check if the number is a valid IRD.

    This checks the length, formatting and check digit.
    """
    number = compact(number)

    if len(number) not in (8, 9):
        raise InvalidLength()

    if not isdigits(number):
        raise InvalidFormat()

    if not 10000000 < int(number) < 150000000:
        raise InvalidFormat()

    if number[-1] != calc_check_digit(number[:-1]):
        raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number is a valid IRD."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join([number[:-6], number[-6:-3], number[-3:]])
