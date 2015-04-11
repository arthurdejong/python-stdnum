# mva.py - functions for handling Norwegian VAT numbers
# coding: utf-8
#
# Copyright (C) 2012, 2013 Arthur de Jong
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

"""MVA nummer (Merverdiavgift, Norwegian VAT number).

The VAT number is standard Norwegian organization number
(organisasjonsnummer) with 'MVA' as suffix. The number is
9-digit code where the last digit is a weighted MOD11 checksum.

>>> validate('NO 995 525 828 MVA')
'995525828'
>>> validate('NO 995 525 829 MVA')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.no import orgnr
from stdnum.exceptions import *
from stdnum.util import clean

# use the same checksum functions as orgnr
checksum = orgnr.checksum
is_valid = orgnr.is_valid


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    if number.startswith('NO'):
        number = number[2:]
    return number


def validate(number):
    """Checks to see if the number provided is a valid organization
    number. This checks the length, formatting and check digit."""
    number = compact(number)
    if not number.endswith('MVA'):
        raise InvalidFormat()
    orgnr.validate(number[:-3])
    return number
