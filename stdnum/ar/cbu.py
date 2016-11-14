# cbu.py - functions for handling Argentinian CBU numbers
# coding: utf-8
#
# Copyright (C) 2016 Luciano Rossi
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

"""CBU (Clave Bancaria Uniforme).

CBU it s a code of the Banks of Argentina to identify the accounts
of their clients.

>>> validate('2850590940090418135201')
'2850590940090418135201'
>>> validate('285059094009041')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('A850590940090418135201')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('2810590940090418135201')
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
    ponderador = '9713'
    bloque_valor = number[:-1]
    bloque_digito = int(number[-1])
    largo_valor = len(bloque_valor)
    suma = 0
    digito_ponderador = 3

    for count in range(largo_valor):
        indice = -1 - count
        valor = int(bloque_valor[indice])
        ponderacion = int(ponderador[digito_ponderador])

        suma += valor * ponderacion
        if digito_ponderador > 0:
            digito_ponderador = digito_ponderador - 1
        else:
            digito_ponderador = 3

    bloque_suma = 10 - (suma % 10)
    digito = int(str(bloque_suma)[-1])
    return digito == bloque_digito


def validate(number):
    """Checks to see if the number provided is a valid CBU."""
    number = compact(number)
    if len(number) != 22:
        raise InvalidLength()
    if not number.isdigit():
        raise InvalidFormat()
    if not calc_check_digit(number[:8]):
        raise InvalidChecksum()
    if not calc_check_digit(number[8:]):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid CBU."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
