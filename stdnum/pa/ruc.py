# ruc.py - functions for handling Panama RUC numbers
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

"""RUC (Registro Único del Contribuyente, Panama tax number).

The Registro Único del Contribuyente (RUC) is an identifier of legal entities
for tax purposes.

This number has different variants both for natural and legal persons, each
with its own structure, but basically it consists on a number of digits and
letters (only for natural persons) usually separated by hyphens (the number and
position of these varies according to the variant), then followed by a check
number (dígito verificador) consisting in up to two digits.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Panama-TIN.pdf
* https://studylib.es/doc/545131/algoritmo-para-el-calculo-del-digito-verificador-de-la-ru

>>> validate('253-92-57027 DV 76')
'00000002530092057027DV76'
>>> validate('155587169-2-2014    D.V. 9')
'01555871690002002014DV09'
>>> validate('253-92-57027 DV 23')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('12345678')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('253-92-57027 DV 76')
'0000000253-0092-057027 DV76'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


ARRVAL = {
    '00': '00',
    '10': '01',
    '11': '02',
    '12': '03',
    '13': '04',
    '14': '05',
    '15': '06',
    '16': '07',
    '17': '08',
    '18': '09',
    '19': '01',
    '20': '02',
    '21': '03',
    '22': '04',
    '23': '07',
    '24': '08',
    '25': '09',
    '26': '02',
    '27': '03',
    '28': '04',
    '29': '05',
    '30': '06',
    '31': '07',
    '32': '08',
    '33': '09',
    '34': '01',
    '35': '02',
    '36': '03',
    '37': '04',
    '38': '05',
    '39': '06',
    '40': '07',
    '41': '08',
    '42': '09',
    '43': '01',
    '44': '02',
    '45': '03',
    '46': '04',
    '47': '05',
    '48': '06',
    '49': '07',
}


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    parts = clean(number, ' .').strip().upper().split('-')

    # We can currently only compact legal person's RUC numbers with check digit.
    if len(parts) != 3 or len(parts[0]) in (1, 2) or 'DV' not in parts[2]:
        return ''

    parts[2], dv = parts[2].split('DV')

    return ''.join([parts[0].zfill(10), parts[1].zfill(4),
                    parts[2].strip().zfill(6), 'DV', dv.strip().zfill(2)])


def calc_check_digit(number, is_old_legal_ruc):
    """Calculate the check digit."""
    if is_old_legal_ruc:
        weights = list(range(2, 12)) + list(range(11, len(number) + 1))
    else:
        weights = list(range(2, len(number) + 2))
    total = sum(int(n) * w for w, n in zip(weights, reversed(number)))
    r = total % 11
    return str(11 - r) if r > 1 else '0'


def validate(number):
    """Check if the number is a valid Panama RUC number.

    This checks the length, formatting and check digits.
    """
    number = compact(number)
    if len(number) != 24:
        raise InvalidLength()
    if not isdigits(number[:-4]) or not isdigits(number[-2:]):
        raise InvalidComponent()
    is_old_legal_ruc = number[3:6] in ('000', '001', '002', '003', '004')
    if is_old_legal_ruc and number[5:7] in ARRVAL:
        number = number[:5] + ARRVAL[number[5:7]] + number[7:]
    dv1 = calc_check_digit(number[:-4], is_old_legal_ruc)
    if number[-2] != dv1:
        raise InvalidChecksum()
    dv2 = calc_check_digit(number[:-4] + dv1, is_old_legal_ruc)
    if number[-1] != dv2:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid Panama RUC number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return ''.join([number[:10], '-', number[10:14], '-', number[14:-4], ' ',
                    number[-4:]])
