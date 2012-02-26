# siren.py - functions for handling French SIREN numbers
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

"""SIREN (a French company identification number).

The SIREN (Système d'Identification du Répertoire des Entreprises) is a 9
digit number used to identify French companies. The Luhn checksum is used
to validate the numbers.

>>> compact('552 008 443')
'552008443'
>>> is_valid('404833048')
True
>>> is_valid('404833047')
False
"""

from stdnum.util import clean
from stdnum import luhn


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' ').strip()


def is_valid(number):
    """Checks to see if the number provided is a valid number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 9 and number.isdigit() and luhn.is_valid(number)
