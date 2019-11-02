# esr.py - functions for handling Swiss EinzahlungsSchein mit Referenznummer
# coding: utf-8
#
# Copyright (C) 2019 Arthur de Jong
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

"""ESR, ISR, QR-reference (Eizahlungsschein mit Referenznummer,
                           pay-in slip with reference number)

The Swiss ESR/ISR/QR-reference is a reference number used on payment slips. 

An ISR (inpayment slip with reference number) refers to the orange payment
slip in Switzerland with which money can be transferred to an account. It
contains a machine-readable encoding line that contains a participant number
and reference number. The participant number ensures the crediting to the
corresponding Post account. The reference number enables the creditor to
identify the invoice recipient. In this way, the payment process can be
handled entirely electronically, from the invoicing date to the booking of
the amount at the creditor.

It consists of 26 numerical characters followed by a Modulo 10 recursive check
digit. It is printed in blocks of 5 characters (beginning with 2 characters,
then 5x5-character groups). Leading zeros digits can be omitted.

This module always prints all digits, including optional leading zeros, so
it is compatible with the newer QR-reference.

More information:

* https://www.paymentstandards.ch/dam/downloads/ig-qr-bill-en.pdf

>>> validate('21 00000 00003 13947 14300 09017')
'210000000003139471430009017'
>>> validate('210000000003139471430009017')
'210000000003139471430009017'
>>> validate('210000000003139471430009016')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('210000000003139471430009017')
'21 00000 00003 13947 14300 09017'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips
    surrounding whitespace and separators."""
    return clean(number, ' ').strip()


def calc_check_digit(number, carry_over='0', alphabet='0946827135'):
    """Calculate the check digit for number. The number passed should
    not have the check digit included."""
    number = compact(number)
    if len(number) == 0:
        return (str((10-int(carry_over))%10))
    new_alphabet = alphabet[int(carry_over):] + alphabet[:int(carry_over)]
    new_carry_over = new_alphabet[int(number[0])]
    return (calc_check_digit(number[1:], new_carry_over))


def validate(number):
    """Check if the number is a valid ESR. This checks the length, formatting
    and check digit."""
    number = compact(number)
    if len(number) > 27:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    if number[-1] != calc_check_digit(number[:-1]):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid ESR."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = 27*"0" + compact(number)
    number = number[-27:]
    return number[:2] + ' ' + ' '.join(
        number[i:i + 5] for i in range(2, len(number), 5))
