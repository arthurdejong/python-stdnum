# ubn.py - functions for handling Ukrainian RNOKPP numbers
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

"""RNTRC (Registration Number of the Taxpayer's Registration Card) or РНОКПП
(Реєстраційний номер облікової картки платника податків), or RNOKPP.

The RNTRC (РНОКПП) is a unique identification number that is provided to
individuals - payers of taxes and other mandatory payments and is retained by
them throughout their lives. The number consists of 10 digits, the last being
a check digit.

More information:

* https://uk.wikipedia.org/wiki/%D0%A0%D0%B5%D1%94%D1%81%D1%82%D1%80%D0%B0%D1%86%D1%96%D0%B9%D0%BD%D0%B8%D0%B9_%D0%BD%D0%BE%D0%BC%D0%B5%D1%80_%D0%BE%D0%B1%D0%BB%D1%96%D0%BA%D0%BE%D0%B2%D0%BE%D1%97_%D0%BA%D0%B0%D1%80%D1%82%D0%BA%D0%B8_%D0%BF%D0%BB%D0%B0%D1%82%D0%BD%D0%B8%D0%BA%D0%B0_%D0%BF%D0%BE%D0%B4%D0%B0%D1%82%D0%BA%D1%96%D0%B2

>>> validate('1759013776')
'1759013776'
>>> validate('1759013770')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format(' 25 30 41 40 71 ')
'2530414071'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This removes surrounding whitespace and ensures it is 8 characters long.
    """
    return clean(number, ' ').strip()


def calc_checksum(number):
    """Calculate the checksum over the number."""
    weights = (-1, 5, 7, 9, 4, 6, 10, 5, 7)
    total = sum(w * int(n) for w, n in zip(weights, number))
    return (total % 11) % 10


def validate(number):
    """Check if the number is a valid Ukraine RNOKPP (РНОКПП) number.

    This checks the length, formatting and check digit.
    """
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    checksum = calc_checksum(number)
    if int(number[-1]) != checksum:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid Ukraine RNOKPP (РНОКПП) number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
