# rcs.py - functions for handling French NIR numbers
# coding: utf-8
#
# Copyright (C) 2025
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

"""RCS (French registration number for commercial companies).

The RCS number (Registre du commerce et des sociétés) is given by INSEE to a company with commercial activity 
when created. It is required for most of administrative procedures.

The number consists of "RCS" letters followed by name of the city where the company was registered
followed by letter A for a retailer or B for society
followed by the SIREN number

More information:

* https://entreprendre.service-public.fr/vosdroits/F31190

>>> validate('RCS Nancy B 323 159 715')
'RCS Nancy B 323 159 715'
>>> validate('RCS Nancy B 323159715')
'RCS Nancy B 323 159 715'
>>> validate('RCS Nancy B323 159715')
'RCS Nancy B 323 159 715'
>>> validate('RCS Nancy B 323 159 716')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('6546546546546703')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('RCSNancy B 323 159 716')  # invalid format
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('RCS NancyB 323 159 716')  # invalid format
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> format('RCS Nancy B323159716')
'RCS Nancy B 323 159 715'
>>> to_siren("RCS Nancy B 323159 716")
"323159 716"
"""

from __future__ import annotations
import re

from stdnum.exceptions import *
from stdnum.fr import siren
from stdnum.util import isdigits

RCS_VALIDATION_REGEX = r"^ *(?P<tag>RCS|rcs) +(?P<city>.*?) +(?P<letter>[AB]) *(?P<siren>(?:\d *){9})\b *$"

def validate(number:str) -> str:
    match = re.match(RCS_VALIDATION_REGEX, number)
    if not match:
        raise InvalidFormat()
    siren_number = siren.validate(match.group("siren"))
    siren_number = siren.format(siren_number)

    return format(number)


def is_valid(number: str) -> bool:
    """Check if the number provided is valid."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number: str) -> str:
    """Reformat the number to the standard presentation format."""
    match = re.match(RCS_VALIDATION_REGEX, number)
    if not match:
        raise InvalidFormat()
    return " ".join(("RCS", match.group('city'), match.group('letter'), siren.format(match.group('siren'))))


def to_siren(number:str)->str:
    """Extract SIREN number from the RCS number.

    The SIREN number is the 9 last digits of the RCS number.
    """
    _siren: list[str] = []
    digit_count = 0
    for char in reversed(number):
        if digit_count < 9:
            _siren.insert(0,char)
            if isdigits(char):
                digit_count += 1
    return ''.join(_siren)
