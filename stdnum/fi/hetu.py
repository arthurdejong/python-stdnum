# hetu.py - functions for handling Finnish personal identity codes
# coding: utf-8
#
# Copyright (C) 2011 Jussi Judin
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

"""HETU (Henkilötunnus, Finnish personal identity code).

Module for handling Finnish personal identity codes (HETU, Henkilötunnus).
See http://www.vaestorekisterikeskus.fi/default.aspx?id=45 for checksum
calculation details and http://tarkistusmerkit.teppovuori.fi/tarkmerk.htm#hetu1
for historical details.

>>> is_valid('131052-308T')
True
>>> is_valid('131052-308U')
False
>>> is_valid('310252-308Y')
False
>>> compact('131052a308t')
'131052A308T'
"""

import re
import datetime


_century_codes = {
    '+': 1800,
    '-': 1900,
    'A': 2000,
    }

# Finnish personal identity codes are composed of date part, century
# indicating sign, individual number and control character.
# ddmmyyciiiC
_hetu_re = re.compile(r'^(?P<day>[0123]\d)(?P<month>[01]\d)(?P<year>\d\d)'
                      r'(?P<century>[-+A])(?P<individual>\d\d\d)'
                      r'(?P<control>[0-9ABCDEFHJKLMNPRSTUVWXY])$')


def compact(number):
    """Convert the HETU to the minimal representation. This strips
    surrounding whitespace and converts it to upper case."""
    return number.strip().upper()


def _calc_checksum(number):
    return '0123456789ABCDEFHJKLMNPRSTUVWXY'[int(number) % 31]


def is_valid(number):
    """Checks to see if the number provided is a valid HETU. It checks the
    format, whether a valid date is given and whether the check digit is
    correct."""
    try:
        match = _hetu_re.search(compact(number))
        if not match:
            return False
    except:
        return False
    day = int(match.group('day'))
    month = int(match.group('month'))
    year = int(match.group('year'))
    century = _century_codes[match.group('century')]
    individual = int(match.group('individual'))
    # check if birth date is valid
    try:
        datetime.date(century + year, month, day)
    except ValueError, e:
        return False
    # for historical reasons individual IDs start from 002
    if individual < 2:
        return False
    checkable_number = '%02d%02d%02d%03d' % (day, month, year, individual)
    return match.group('control') == _calc_checksum(checkable_number)


# This is here just for completeness as there are no different length forms
# of Finnish personal identity codes:
format = compact
