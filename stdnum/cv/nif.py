# nif.py - functions for handling Cape Verde NIF numbers
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

"""NIF (Número de Identificação Fiscal, Cape Verde tax number).

This number consists of 9 digits, sometimes separated into three groups with
three digits each to make it easier to read, like XXX XXX XXX.

The first digit indicates the type of person:

  * 1: Singular person, either resident or non resident.
  * 2: Companies.
  * 3: National entities.
  * 4: International entities.
  * 5: Other entities.

The following six digits are either:

  * The Bilhete de Identidade number, for singular resident persons, or
  * A sequence automatically assigned, for all other cases.

The last two digits are control digits.

More information:

* https://portondinosilhas.gov.cv/images/igrp-portal/img/documentos/EA834694B09A15FAE044002128A60A02.pdf
* https://www.mf.gov.cv/documents/54571/273413/adenda_esclarecimentos_pdfs.pdf


>>> validate('200129775')
'200129775'
>>> validate('200 144 731')
'200144731'
>>> validate('253.656.575')
'253656575'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('VV3456789')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('923456789')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> format('200 144 731')
'200144731'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -.').strip()


def validate(number):
    """Check if the number is a valid Cape Verde NIF number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[0] not in ('1', '2', '3', '4', '5'):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid Cape Verde NIF number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
