# cvr.py - functions for handling Danish CVR numbers
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

"""CVR (Momsregistreringsnummer, Danish VAT number).

The CVR (Momsregistreringsnummer, VAT) is an 8 digit number with a
straightforward check mechanism.

>>> compact('DK 13585628')
'13585628'
>>> is_valid('DK 13585628')
True
>>> is_valid('DK 13585627')
False
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.,/:').upper().strip()
    if number.startswith('DK'):
        number = number[2:]
    return number


def checksum(number):
    """Calculate the checksum."""
    weights = (2, 7, 6, 5, 4, 3, 2, 1)
    return sum(weights[i] * int(n) for i, n in enumerate(number)) % 11


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 8 and number.isdigit() and \
           number[0] != '0' and checksum(number) == 0
