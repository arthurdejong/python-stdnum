# vat.py - functions for handling Swiss social security numbers
#
# Copyright (C) 2014 Denis Krienbuehl
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

"""Swiss social security number ("Sozialversicherungsnummer").

Also known as "Neue AHV Nummer".

The Swiss Sozialversicherungsnummer is used to identify indivduals for taxation
and pension purposes.

The number is validated using EAN-13, though dashes are substitued for dots.

>>> compact('756.9217.0769.85')
'7569217076985'
>>> format('7569217076985')
'756.9217.0769.85'
>>> validate('7569217076985')
'7569217076985'
>>> validate('756.9217.0769.85')
'7569217076985'
>>> validate('756.9217.0769.84')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.exceptions import ValidationError
from stdnum import ean
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' .').strip()


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return '.'.join((number[:3], number[3:7], number[7:11], number[11:]))


def validate(number):
    """Checks to see if the number provided is a valid
    Swiss Sozialversicherungsnummer."""
    return ean.validate(compact(number))


def is_valid(number):
    """Checks to see if the number provided is a valid
    Sozialversicherungsnummer."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
