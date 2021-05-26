# cc.py - functions for handling Portuguese Identity numbers
# coding: utf-8
#
# Copyright (C) 2021 David Vaz
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

"""CC (Número de Cartão de Cidadão, Portuguese Identity number).

The Portuguese Identity Number is alfa numeric with the following format:

DDDDDDDD C AAT

with:
D - Civil Identity Number [0-9]
C - Civil Identity Number Check Digit [0-9]
A - Version [A-Z0-9]
T - Identity Number Check Digit [0-9]

Full definition in Portuguese can be found here:
https://www.autenticacao.gov.pt/documents/20126/115760/Valida%C3%A7%C3%A3o+de+N%C3%BAmero+de+Documento+do+Cart%C3%A3o+de+Cidad%C3%A3o.pdf

>>> validate('00000000 0 ZZ4')
'000000000ZZ4'
>>> validate('00000000 A ZZ4')  # invalid format
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('00000000 0 ZZ3')  # invalid check digits
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""
import re

from stdnum.exceptions import *
from stdnum.util import clean, isdigits

_cc_re = re.compile(r'^\d*[A-Z0-9]{2}\d$')


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    return number


def _alphabet_convert(char):
    """
    alphabet table conversion:
    0: 0, .. 9: 9
    A:10, B: 11 .. Z:35
    """
    if isdigits(char):
        return ord(char) - ord('0')
    return ord(char) - ord('A') + 10


def validate(number):
    """checks if the number is a valid cartao de cidadao number"""
    number = compact(number)

    if not _cc_re.match(number):
        raise InvalidFormat()

    value_sum = 0
    for i in range(len(number) - 1, -1, -1):
        value = _alphabet_convert(number[i])
        if i % 2 == 0:
            value *= 2
            if value > 9:
                value -= 9
        value_sum += value

    if value_sum % 10 != 0:
        raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return ' '.join([number[:-4], number[-4], number[-3:]])
