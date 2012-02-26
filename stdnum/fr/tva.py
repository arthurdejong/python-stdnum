# tva.py - functions for handling French TVA numbers
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

"""n° TVA (taxe sur la valeur ajoutée, French VAT number).

The n° TVA (Numéro d'identification à la taxe sur la valeur ajoutée) is the
SIREN (Système d’Identification du Répertoire des Entreprises) prefixed by
two digits. In old style numbers the two digits are numeric, with new
style numbers at least one is a alphabetic.

>>> compact('Fr 40 303 265 045')
'40303265045'
>>> is_valid('23334175221')
True
>>> is_valid('84 323 140 391')  # incorrect check digit
False
>>> is_valid('K7399859412')  # new-style number
True
>>> is_valid('4Z123456782')  # new-style number starting with digit
True
"""

from stdnum.util import clean
from stdnum.fr import siren


# the valid characters for the first two digits (O and I are missing)
_alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('FR'):
        number = number[2:]
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if len(number) == 11 and siren.is_valid(number[2:]) and \
       number[0] in _alphabet and number[1] in _alphabet:
        if number.isdigit():
            # all-numeric digits
            return int(number[:2]) == int(number[2:] + '12') % 97
        else:
            # one of the first two digits isn't a number
            if number[0].isdigit():
                check = _alphabet.index(number[0]) * 24 + \
                        _alphabet.index(number[1]) - 10
            else:
                check = _alphabet.index(number[0]) * 34 + \
                        _alphabet.index(number[1]) - 100
            return (int(number[2:]) + 1 + check // 11 ) % 11 == check % 11
    else:
        return False
