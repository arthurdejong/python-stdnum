# coding=utf-8
# nn.py - function for handling Belgian national numbers
#
# Copyright (C) 2021 Cédric Krier
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

"""NN, NISS (Belgian national number).

The national number is a unique identifier of Belgian. The number consists of
11 digits.

More information:

* https://fr.wikipedia.org/wiki/Numéro_de_registre_national

>>> compact('85.07.30-033 28')
'85073003328'
>>> validate('85 07 30 033 28')
'85073003328'
>>> validate('17 07 30 033 84')
'17073003384'
>>> validate('12345678901')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('85073003328')
'85.07.30-033.28'
"""

import datetime

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the number
    of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').strip()
    return number


def _checksum(number):
    """Calculate the checksum."""
    numbers = [number]
    if int(number[:2]) + 2000 <= datetime.date.today().year:
        numbers.append('2' + number)
    for n in numbers:
        if 97 - (int(n[:-2]) % 97) == int(n[-2:]):
            return True
    return False


def validate(number):
    """Check if the number if a valid National Number."""
    number = compact(number)
    if not isdigits(number) or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    if not _checksum(number):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid National Number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return (
        '.'.join(number[i:i + 2] for i in range(0, 6, 2)) +
        '-' + '.'.join([number[6:9], number[9:11]]))
