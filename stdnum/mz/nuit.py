# nuit.py - functions for handling Mozambique NUIT numbers
# coding: utf-8
#
# Copyright (C) 2023 Leandro Regueiro
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

"""NUIT (Número Único de Identificação Tributaria, Mozambique tax number).

This number consists of 9 digits, sometimes separated in three groups of three
digits using whitespace to make it easier to read.

The first digit indicates the type of entity. The next seven digits are a
sequential number. The last digit is the check digit, which is used to verify
the number was correctly typed.

More information:

* https://www.mobilize.org.mz/nuit-numero-unico-de-identificacao-tributaria/
* http://www.at.gov.mz/por/Perguntas-Frequentes2/NUIT

>>> validate('400339910')
'400339910'
>>> validate('400 005 834')
'400005834'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('400339910')
'400 339 910'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -.').strip()


def validate(number):
    """Check if the number is a valid Mozambique NUIT number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Mozambique NUIT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return ' '.join([number[:3], number[3:-3], number[-3:]])
