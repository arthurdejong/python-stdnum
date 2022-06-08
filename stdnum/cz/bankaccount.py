# bankaccount.py - functions for handling Czech bank account numbers
# coding: utf-8
#
# Copyright (C) 2022 Arthur de Jong
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

"""Czech bank account number

The Czech bank account numbers consist of up to 20 digits:
    UUUUUK-MMMMMMMMKM/XXXX

The first part is prefix that is up to 6 digits. The following part is from 2 to 10 digits.
Both parts could be filled with zeros from left if missing.
The final 4 digits represent the bank code.

More information:

* https://www.penize.cz/osobni-ucty/424173-tajemstvi-cisla-uctu-klicem-pro-banky-je-11
* http://www.zlatakoruna.info/zpravy/ucty/cislo-uctu-v-cr

>>> validate('34278-0727558021/0100')
'034278-0727558021/0100'
>>> validate('4278-727558021/0100')  # invalid check digits (prefix)
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('34278-727558021/0000')  # invalid bank
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> format('34278-727558021/0100')
'034278-0727558021/0100'
"""

import re

from stdnum.exceptions import (
    InvalidChecksum, InvalidComponent, InvalidFormat, ValidationError)
from stdnum.util import clean


_prefix_regex = r'[0-9]{0,6}'
_root_regex = r'[0-9]{2,10}'
_bank_regex = r'[0-9]{4}'
_regex = r'((%s)-)?(%s)\/(%s)' % (_prefix_regex, _root_regex, _bank_regex)

_root_weights = [6, 3, 7, 9, 10, 5, 8, 4, 2, 1]
_prefix_weights = _root_weights[4:]  # prefix weights are same as root, but we are interested in last 6 weights only


def _parse(number):
    number = clean(number).strip()
    match = re.match(_regex, number)
    if match:
        prefix = match.group(2)
        root = match.group(3)
        bank = match.group(4)
        return prefix, root, bank


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    parsed = _parse(number)
    if parsed:
        prefix, root, bank = parsed
        return ''.join((
            prefix + '-' if prefix else '', root, '/', bank,
        ))


def _info(bank_code):
    from stdnum import numdb
    info = {}
    for nr, found in numdb.get('cz/banks').info(bank_code):
        info.update(found)
    return info


def info(number):
    """Return a dictionary of data about the supplied number. This typically
    returns the name of the bank and branch and a BIC if it is valid."""
    parsed = _parse(number)
    if parsed:
        return _info(parsed[2])


def _get_checksum(part):
    if len(part) > 6:
        weights = _root_weights
        part.zfill(10)
    else:
        weights = _prefix_weights
        part.zfill(6)

    _sum = 0
    for i, n in enumerate(part):
        _sum += weights[i] * int(n)

    return _sum % 11


def is_checksum_valid(part):
    """Check if prefix or root of bank account number is valid."""
    return _get_checksum(part) == 0


def is_bank_valid(bank_code):
    """Check if bank code is valid."""
    return 'bank' in _info(bank_code)


def validate(number):
    """Check if the number provided is a valid bank account number."""
    number = format(number)  # fill missing zeros
    if not number:
        raise InvalidFormat()

    prefix, root, bank = _parse(number)

    if not is_checksum_valid(prefix):
        raise InvalidChecksum()

    if not is_checksum_valid(root):
        raise InvalidChecksum()

    if not is_bank_valid(bank):
        raise InvalidComponent()

    return number


def is_valid(number):
    """Check if the number provided is a valid bank account number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    parsed = _parse(number)
    if parsed:
        return ''.join((
            (parsed[0] or '').zfill(6), '-', parsed[1].zfill(10), '/', parsed[2],
        ))
