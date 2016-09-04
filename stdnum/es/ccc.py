# ccc.py - functions for handling Spanish CCC bank account code
# coding: utf-8
#
# Copyright (C) 2016 David García Garzón
# Copyright (C) 2016 Arthur de Jong
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

"""CCC (Código Cuenta Corriente, Bank Account Code)

CCC code is the country specific part in spanish IBAN codes.
In order to fully validate an Spanish IBAN you have
to validate as well the country specific part as a valid CCC.
It was used alone without the IBAN add-on for home banking
transactions until Febrary 1st 2014 when IBAN codes started
to be used as all purpose account ID.

CCC has 20 digits, all being numbers: EEEE OOOO DD NNNNNNNNNN

* EEEE: Banking entity
* OOOO: Office
* DD: Control digits
* NNNNN NNNNN: Account

This module does NOT check for the bank code to exist.
Existing bank codes are published on the 'Registro de Entidades'
by 'Banco de España' (Spanish Central Bank).

More information:

* https://es.wikipedia.org/wiki/C%C3%B3digo_cuenta_cliente
* http://goo.gl/MaJ5PS (Registro Entidades del Banco de España)


>>> compact('1234-1234-16 1234567890')
'12341234161234567890'

>>> format('12341234161234567890')
'1234 1234 16 12345 67890'

>>> validate('1234-1234-16 1234567890')
'12341234161234567890'

>>> validate('134-1234-16 1234567890') # wrong size
Traceback (most recent call last):
    ...
InvalidLength: Length should be 20

>>> validate('12X4-1234-16 1234567890') # non numbers
Traceback (most recent call last):
    ...
InvalidFormat: All digits should be numbers

>>> validate('1234-1234-00 1234567890') # invalid control digits
Traceback (most recent call last):
    ...
InvalidChecksum: Invalid control digits, expected 16 got 00

>>> is_valid('1234-1234-16 1234567890') # a fancy valid number
True
>>> is_valid('1234-1234-00 1234567890') # altering control makes it not valid
False
>>> is_valid('1111-2222-06 1234567890') # change bank-office and its control
True
>>> is_valid('1234-1234-10 1111111111') # change account and its control
True
>>> is_valid('1111-2222-00 3333333333') # change both sides
True

"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    return clean(number, ' -').strip()


def format(number):
    number = compact(number)
    return ' '.join([
        number[0:4],
        number[4:8],
        number[8:10],
        number[10:15],
        number[15:20],
        ])


def validate(number):
    """Checks to see if the number provided is a valid CCC."""
    def DC(digits):
        dc = 11 - sum(int(d) * 2**i for i, d in enumerate(digits)) % 11
        return str(dc if dc < 10 else 11 - dc)

    number = compact(number)

    if len(number) != 20:
        raise InvalidLength("Length should be 20")

    if not number.isdigit():
        raise InvalidFormat("All digits should be numbers")

    bank, office, dc, account = (
        number[:4], number[4:8], number[8:10], number[10:])
    expectedDc = DC('00'+bank+office) + DC(account)
    if dc != expectedDc:
        raise InvalidChecksum(
            "Invalid control digits, expected {} got {}"
            .format(expectedDc, dc))

    # TODO: Check the for the bank code and raise InvalidComponent
    # and raise InvalidComponent if it does not exist.

    return number


def is_valid(number):
    """Checks to see if the number provided is a valid CCC."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
