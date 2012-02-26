# vat.py - functions for handling Bulgarian VAT numbers
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

"""VAT (Идентификационен номер по ДДС, Bulgarian VAT number).

The Bulgarian VAT (Данък върху добавената стойност) number is either 9
(for legal entities) or 10 digits (for physical persons, foreigners and
others) long. Each type of number has it's own check digit algorithm.

>>> compact('BG 175 074 752')
'175074752'
>>> is_valid('175074752')
True
>>> is_valid('175074751')  # invalid check digit
False
"""

from stdnum.util import clean
from stdnum.bg import egn, pnf


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('BG'):
        number = number[2:]
    return number


def calc_check_digit_legal(number):
    """Calculate the check digit for legal entities. The number passed
    should not have the check digit included."""
    check = sum((i + 1) * int(n) for i, n in enumerate(number)) % 11
    if check == 10:
        check = sum((i + 3) * int(n) for i, n in enumerate(number)) % 11
    return str(check % 10)


def calc_check_digit_other(number):
    """Calculate the check digit for others. The number passed should not
    have the check digit included."""
    weights = (4, 3, 2, 7, 6, 5, 4, 3, 2)
    return str((11 - sum(weights[i] * int(n) for i, n in enumerate(number))) % 11)


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if len(number) == 9 and number.isdigit():
        # 9 digit numbers are for legal entities
        return number[-1] == calc_check_digit_legal(number[:-1])
    if len(number) == 10 and number.isdigit():
        # 10 digit numbers are for physical persons, foreigners and others
        return egn.is_valid(number) or \
               pnf.is_valid(number) or \
               number[-1] == calc_check_digit_other(number[:-1])
    return False
