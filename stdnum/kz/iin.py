# iin.py - functions for handling Kazakhstani individual identification numbers
# coding: utf-8
#
# Copyright (C) 2026 Luca Sicurello
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
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

"""IIN (ЖСН, Жеке сәйкестендіру нөмірі, Kazakhstani Individual identification number).

It is a 12-digit number of which the first 6 digits denote the person's
birth date in the format YYMMDD, the next digit encodes the gender and
century of birth, the next four digits represent a birth serial number
and the last digit is a check digit.

* https://www.gov.kz/article/648?lang=kk
* https://ru.wikipedia.org/wiki/Индивидуальный_идентификационный_номер


>>> compact('921029 35085 1')
'921029350851'
>>> validate('921029350851')
'921029350851'
>>> get_birth_date('921029350851')
datetime.date(1992, 10, 29)
>>> validate('92102B50851')  # invalid digit
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('921529350859')  # invalid date
Traceback (most recent call last):
    ...
InvalidComponent: ...
"""

from __future__ import annotations

import datetime

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number: str) -> str:
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' ')


def calc_check_digit(number: str) -> str:
    """Calculate the check digit. The number passed should not have
    the check digit included."""
    s = sum(w * int(n) for w, n in zip(range(1, 12), number[:11])) % 11
    if s != 10:
        return str(s)

    s = sum(w * int(n) for w, n in zip(range(3, 14), number[:11])) % 11
    if s != 10:
        return str(s)

    raise InvalidComponent()


def get_birth_date(number: str) -> datetime.date:
    """Get the birth date from the person's Individual identification number."""
    number = compact(number)
    year = int(number[0:2])
    month = int(number[2:4])
    day = int(number[4:6])

    if number[6] == '0':  # no century info for foreign nationals
        today = datetime.date.today()
        year += (today.year // 100) * 100
        if year >= today.year:
            year -= 100

    elif number[6] in '12':
        year += 1800
    elif number[6] in '34':
        year += 1900
    elif number[6] in '56':
        year += 2000
    else:
        raise InvalidComponent()

    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise InvalidComponent()


def get_gender(number: str) -> str | None:
    """Get the gender of the person's Individual identification number."""
    number = compact(number)
    if number[6] == '0':
        return None
    elif int(number[6]) % 2:
        return 'M'
    else:
        return 'F'


def validate(number: str) -> str:
    """Check if the given Individual identification number is valid.
    This checks the length and whether the check digit is correct."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 12:
        raise InvalidLength()
    if get_birth_date(number) > datetime.date.today():
        raise InvalidComponent()
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number: str) -> bool:
    """Check if the given Individual identification number is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
