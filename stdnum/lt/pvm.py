# pvm.py - functions for handling Lithuanian VAT numbers
# coding: utf-8
#
# Copyright (C) 2012 Arthur de Jong
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

"""PVM (Pridėtinės vertės mokestis mokėtojo kodas, Lithuanian VAT number).

The PVM is used for VAT purposes in Lithuania. It is 9 digits (for legal
entities) or 12 digits long (for temporarily registered taxpayers). This
module does not check the format of Lithuanian personal codes (Asmens
kodas).

>>> compact('LT 100001919017')
'100001919017'
>>> is_valid('119511515')  # organisation
True
>>> is_valid('100001919017')  # temporarily registered
True
>>> is_valid('100001919018')  # invalid check digit
False
>>> is_valid('100004801610')  # second step in check digit calculation
True
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('LT'):
        number = number[2:]
    return number


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    check = sum((1 + i % 9) * int(n) for i, n in enumerate(number)) % 11
    if check == 10:
        check = sum((1 + (i + 2) % 9) * int(n) for i, n in enumerate(number))
    return str(check % 11 % 10)


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if not number.isdigit():
        return False
    if len(number) == 9:
        # legal entities
        return number[7] == '1' and \
               calc_check_digit(number[:-1]) == number[-1]
    if len(number) == 12:
        # temporary tax payers and natural persons
        return number[10] == '1' and \
               calc_check_digit(number[:-1]) == number[-1]
    return False
