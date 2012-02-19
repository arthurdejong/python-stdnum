# vat.py - functions for handling European VAT numbers
# coding: utf-8
#
# Copyright (C) 2012 Arthur de Jong
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

"""Module for handling various European VAT numbers.

>>> is_valid('ATU 57194903')
True
>>> is_valid('BE697449992')
True
>>> compact('FR 61 954 506 077')
'FR61954506077'
>>> guess_country('00449544B01')
['nl']
"""


country_codes = set([
    'at', 'be', 'bg', 'cy', 'cz', 'de', 'dk', 'ee', 'es', 'fi', 'fr', 'gb',
    'gr', 'hu', 'ie', 'it', 'lt', 'lu', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro',
    'se', 'si', 'sk'
])
"""The collection of country codes that are queried."""

_country_modules = dict()


def _get_cc_module(cc):
    """Get the VAT number module based on the country code."""
    # Greece uses a "wrong" country code
    cc = cc.lower()
    if cc == 'el':
        cc = 'gr'
    if cc not in country_codes:
        return
    if cc not in _country_modules:
        # do `from stdnum.CC import vat` instead of `import stdnum.CC.vat`
        # to handle the case where vat is an alias
        _country_modules[cc] = __import__(
            'stdnum.%s' % cc, globals(), locals(), ['vat']).vat
    return _country_modules[cc]


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = number.upper().strip()
    return number[:2] + _get_cc_module(number[:2]).compact(number[2:])


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    performs the country-specific check for the number."""
    try:
        number = compact(number)
    except:
        return False
    module = _get_cc_module(number[:2])
    return bool(module) and module.is_valid(number[2:])


def guess_country(number):
    """Guess the country code based on the provided number. This checks the
    provided number against each of the validation routines and returns
    the list of countries for which it is valid. This returns lower case
    codes and returns gr (instead of el) for Greece."""
    return [cc
            for cc in country_codes
            if _get_cc_module(cc).is_valid(number)]
