# nif.py - functions for handling Spanish NIF (VAT) numbers
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

"""NIF (Número de Identificación Fiscal, Spanish VAT number).

The Spanish VAT number is a 9-digit number where either the first, last
digits or both can be letters.

The number is either a DNI (Documento nacional de identidad, for
Spaniards), a NIE (Número de Identificación de Extranjeros, for
foreigners) or a CIF (Certificado de Identificación Fiscal, for legal
entities and others).

>>> compact('ES B-58378431')
'B58378431'
>>> is_valid('B64717838')
True
>>> is_valid('B64717839')  # invalid check digit
False
>>> is_valid('54362315K')  # resident
True
>>> is_valid('X-5253868-R')  # foreign person
True
"""

from stdnum.util import clean
from stdnum.es import dni, nie, cif


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -').upper().strip()
    if number.startswith('ES'):
        number = number[2:]
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This checks
    the length, formatting and check digit."""
    try:
        number = compact(number)
    except:
        return False
    if len(number) != 9 or not number[1:-1].isdigit():
        return False
    if number[0].isdigit():
        # natural resident
        return dni.is_valid(number)
    if number[0] in 'XYZ':
        # foreign natural person
        return nie.is_valid(number)
    # otherwise it has to be a valid CIF
    return cif.is_valid(number)
