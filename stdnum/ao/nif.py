# nif.py - functions for handling Angola NIF numbers
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

"""NIF (Número de Identificação Fiscal, Angola tax number).

This number has two variants, one for singular persons and another one for
collective persons.

The collective person's number consists of 10 digits.

The singular person's number consists of 14 characters: the first nine are
digits, followed by two letters and ending with three digits.


More information:

* https://portaldocontribuinte.minfin.gov.ao/perguntas-frequentes/cadastro-contribuinte
* https://tin-check.com/en/tin-check-angola/

>>> validate('5000767115')
'5000767115'
>>> validate('000238553CA017')
'000238553CA017'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('500 002 85 50')
'5000028550'
"""  # noqa: E501

import re

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


_nif_singular_re = re.compile(r'^[0-9]{9}[A-Z]{2}[0-9]{3}$')


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -.').upper().strip()


def validate(number):
    """Check if the number is a valid Angola NIF number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) not in (10, 14):
        raise InvalidLength()
    if len(number) == 10 and not isdigits(number):
        raise InvalidFormat()
    if len(number) == 14 and not _nif_singular_re.search(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Angola NIF number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
