# cuit.py - functions for handling Argentinian VAT numbers
# coding: utf-8
#
# Copyright (C) 2009 Mariano Reingart
# Copyright (C) 2011 Sebastián Marró
# Copyright (C) 2008-2011 Cédric Krier
# Copyright (C) 2008-2011 B2CK
# Copyright (C) 2015 Arthur de Jong
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

"""CUIT (Código Único de Identificación Tributaria, Argentinian tax number).

The CUIT is a taxpayer identification number used for VAT (IVA, Impuesto al
Valor Agregado) and other taxes.

>>> validate('200-5536168-2')
'20055361682'
>>> validate('2026756539')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('2026756A393')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('20267565392')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def calc_check_digit(number):
    """Calculate the check digit."""
    weights = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)
    check = sum(w * int(n) for w, n in zip(weights, number)) % 11
    return '012345678990'[11 - check]


def validate(number):
    """Check if the number is a valid CUIT."""
    number = compact(number)
    if len(number) != 11:
        raise InvalidLength()
    if not number.isdigit():
        raise InvalidFormat()
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid CUIT."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
