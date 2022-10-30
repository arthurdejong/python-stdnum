# tn.py - functions for handling Egypt Tax Number numbers
# coding: utf-8
#
# Copyright (C) 2022 Leandro Regueiro
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

u"""Tax Registration Number (الرقم الضريبي, Egypt tax number).

This number consists of 9 digits, usually separated into three groups
using hyphens to make it easier to read, like XXX-XXX-XXX.

More information:

* https://emsp.mts.gov.eg:8181/EMDB-web/faces/authoritiesandcompanies/authority/website/SearchAuthority.xhtml?lang=en

>>> validate('100-531-385')
'100531385'
>>> validate(u'٣٣١-١٠٥-٢٦٨')
'331105268'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('VV3456789')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> format('100531385')
'100-531-385'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


ARABIC_NUMBERS_MAP = {
    # Arabic-indic digits.
    u'٠': u'0',
    u'١': u'1',
    u'٢': u'2',
    u'٣': u'3',
    u'٤': u'4',
    u'٥': u'5',
    u'٦': u'6',
    u'٧': u'7',
    u'٨': u'8',
    u'٩': u'9',
    # Extended arabic-indic digits.
    u'۰': u'0',
    u'۱': u'1',
    u'۲': u'2',
    u'۳': u'3',
    u'۴': u'4',
    u'۵': u'5',
    u'۶': u'6',
    u'۷': u'7',
    u'۸': u'8',
    u'۹': u'9',
}


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace. It also converts arabic numbers.
    """
    return u''.join([unicode(ARABIC_NUMBERS_MAP.get(c, c))
                     for c in clean(number, u' -–/').strip()])


def validate(number):
    """Check if the number is a valid Egypt Tax Number number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) != 9:
        raise InvalidLength()
    if not isdigits(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid Egypt Tax Number number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return u'-'.join([number[:3], number[3:-3], number[-3:]])
