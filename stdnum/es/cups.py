# cups.py - functions for handling Spanish CUPS code
# coding: utf-8
#
# Copyright (C) 2011-2015 Arthur de Jong
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

"""CUPS (Código Unificado de Punto de Suministro, Supply Point Unified Code)

CUPS codes are used in Spain as unique identifier for energy supply points.
They are used both for electricity and pipelined gas.

They have 20 or 22 digits: LL DDDD CCCC CCCC CCCC EE NT

* LL: (letters) Country. (Always 'ES' since it is a national code)
* DDDD: (numbers) Distribution company code (numeric)
* CCCC CCCC CCCC: Identifier within the distribution company (numeric)
* EE: (numbers) check digits
* N: (number) Border point sequence
* T: (letter) Kind of border point
	* 'F': border point
	* 'P': main metering point
	* 'R': redundant metering point
	* 'C': checking metering point
	* 'X'/'Y'/'Z': registering point

More information:

* https://es.wikipedia.org/wiki/C%C3%B3digo_Unificado_de_Punto_de_Suministro

>>> compact('ES 1234-123456789012-jy')
'ES1234123456789012JY'

>>> format('ES1234123456789012JY')
'ES 1234 1234 5678 9012 JY'

>>> format('ES1234123456789012JY1F')
'ES 1234 1234 5678 9012 JY 1 F'

>>> validate('ES 1234-123456789012-JY')
'ES1234123456789012JY'

>>> validate('GB 1234-123456789012-JY')
Traceback (most recent call last):
    ...
ValidationError: Should start with 'ES'

>>> validate('ES 1234-12X456789012-JY')
Traceback (most recent call last):
    ...
ValidationError: Digit 9 should be a number, but was 'X'

>>> validate('ES 1234-12456789012-JY')
Traceback (most recent call last):
    ...
ValidationError: Length should be either 20 or 22

>>> validate('ES 1234-123456789012-JY 1F')
'ES1234123456789012JY1F'

>>> validate('ES 1234-123456789012-JY 1T')
Traceback (most recent call last):
    ...
ValidationError: Point type should be one of F,P,R,C,X,Y,Z but was 'T'

>>> validate('ES 1234-123456789012-JY XF')
Traceback (most recent call last):
    ...
ValidationError: Point number should be a digit but was 'X'

>>> validate('ES 1234-123456789012-XY 1F')
Traceback (most recent call last):
    ...
ValidationError: Control digits should be 'JY' instead of 'XY'

>>> is_valid('ES 1234-123456789012-JY 1F')
True

>>> is_valid('ES 1234-123456789012-XY 1F')
False


"""

from stdnum.exceptions import *
from stdnum.util import clean

def compact(reference):
    return clean(reference, ' -').strip().upper()

def format(reference):
    reference = compact(reference)
    return ' '.join([
        reference[0:2],
        reference[2:6],
        reference[6:10],
        reference[10:14],
        reference[14:18],
        reference[18:20],
        reference[20:21],
        reference[21:22],
        ]).strip()

def validate(reference):
    reference = compact(reference)

    if len(reference) not in (20,22):
        raise ValidationError("Length should be either 20 or 22")

    if reference[:2] != 'ES':
        raise ValidationError("Should start with 'ES'")

    for i,c in enumerate(reference[2:16]):
        if c.isdigit(): continue
        raise ValidationError(
            "Digit {} should be a number, but was '{}'"
            .format(i+3, c))

    pointtypes='FPRCXYZ'
    if reference[20:]:
        pnumber, ptype = reference[20:]
        if ptype not in pointtypes:
            raise ValidationError(
                "Point type should be one of {} but was '{}'"
                .format(
                    ",".join(pointtypes),ptype))
        if not pnumber.isdigit():
            raise ValidationError(
                "Point number should be a digit but was '{}'"
                .format(pnumber))

    check0, check1 = divmod(int(reference[2:18])%529, 23)
    mapping='TRWAGMYFPDXBNJZSQVHLCKE'
    check = mapping[check0] + mapping[check1]
    if reference[18:20] != check:
        raise ValidationError("Control digits should be '{}' instead of '{}'"
            .format(check, reference[18:20]))

    return reference


def is_valid(number):
    """Checks to see if the number provided is a valid Cadastral Reference."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


