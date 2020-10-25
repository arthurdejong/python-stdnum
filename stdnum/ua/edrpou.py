# ubn.py - functions for handling Ukrainian EDRPOU numbers
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

"""USREOU (Unified State Register of Enterprises and Organizations of Ukraine),
or ЄДРПОУ (Єдиного державного реєстру підприємств та організацій України),
or EDRPOU.

The USREOU (ЄДРПОУ) code is a unique identification number of a legal entity in
the Unified State Register of Enterprises and Organizations of Ukraine. The
number consists of 8 digits, the last being a check digit.

More information:

* https://uk.wikipedia.org/wiki/%D0%9A%D0%BE%D0%B4_%D0%84%D0%94%D0%A0%D0%9F%D0%9E%D0%A3
* http://1cinfo.com.ua/Articles/Proverka_koda_po_EDRPOU.aspx

>>> validate('32855961')
'32855961'
>>> validate('32855968')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format(' 32855961 ')
'32855961'
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
    weights = (1, 2, 3, 4, 5, 6, 7)
    if 30000000 < int(number) < 60000000:
        weights = (7, 1, 2, 3, 4, 5, 6)
    total = sum(w * int(n) for w, n in zip(weights, number))
    if total % 11 < 10:
        return total % 11
    # Calculate again with other weights.
    weights = (3, 4, 5, 6, 7, 8, 9)
    if 30000000 < int(number) < 60000000:
        weights = (9, 3, 4, 5, 6, 7, 8)
    total = sum(w * int(n) for w, n in zip(weights, number))
    return total % 11


def validate(number):
    """Check if the number is a valid Ukraine USREOU (ЄДРПОУ) number.

    This checks the length, formatting and check digit.
    """
    number = compact(number)
    if len(number) != 8:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    checksum = calc_checksum(number)
    if checksum == 10 or int(number[-1]) != checksum:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid Ukraine USREOU (ЄДРПОУ) number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
