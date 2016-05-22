# nif.py - functions for handling French tax identification numbers
#
# Copyright (C) 2012, 2016 Arthur de Jong
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

"""NIF (French tax identification number).

The NIF (Numero d'Identification Fiscale) is a 13 digit number. It is
popularly known as "numero fiscal de reference" or "numero SPI".

More information:

* https://ec.europa.eu/taxation_customs/tin/tinByCountry.html

>>> validate('2 95 10 99 126 111 93')
'295109912611193'
>>> validate('295109912611199')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('295109912611193')
'2 95 10 99 126 111 93'
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' ').strip()


def validate(number):
    """Checks the length to see if the number provided is valid."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()
    return number


def is_valid(number):
    """Checks the length to see if the number provided is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return ' '.join((number[:2], number[2:4], number[4:7],
                     number[7:10], number[10:]))
