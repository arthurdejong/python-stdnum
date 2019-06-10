# tin.py - functions for handling South Africa Tax Reference Number
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

"""South Africa Tax Reference Number.

The Tax Reference Number consists of 9 digits, followed by a check digit.

https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/South-Africa-TIN.pdf

Appendix D in
https://c.ymcdn.com/sites/sait.site-ym.com/resource/resmgr/2014_SARS/Draft_SARS_External_BRS_2014.pdf

>>> validate('0001339050')
'0001339050'
>>> validate('ZA 0843089848')
'0843089848'
>>> validate('2449/494/16/0')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('9125568')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('ZA 084308984-8')
'0843089848'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    number = clean(number, ' -/').upper().strip()

    if number.startswith('ZA'):
        return number[2:]

    return number


def calc_check_digit(number):
    """Calculate the check digit.

    The number passed should not have the check digit included.
    """
    # Add even digits.
    total = sum(int(number[i]) for i in (1, 3, 5, 7))

    # Add odd digits.
    for i in (0, 2, 4, 6, 8):
        # If result has more than one digit, add the individual digits
        # together to get a single digit result. Then add result to total.
        total += sum(int(digit) for digit in list(str(int(number[i]) * 2)))

    return str(-total % 10)


def validate(number):
    """Check if the number is a valid South Africa Tax Reference Number.

    This checks the length, formatting and check digit.
    """
    number = compact(number)

    if len(number) != 10:
        raise InvalidLength()

    if not isdigits(number):
        raise InvalidFormat()

    if number[0] not in ('0', '1', '2', '3', '9'):
        raise InvalidFormat()

    if number[-1] != calc_check_digit(number[:-1]):
        raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number is a valid South Africa Tax Reference Number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
