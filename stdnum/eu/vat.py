# vat.py - functions for handling European VAT numbers
# coding: utf-8
#
# Copyright (C) 2012, 2013 Arthur de Jong
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

"""VAT (European Union VAT number).

The European Union VAT number consists of a 2 letter country code (ISO
3166-1, except Greece which uses EL) followed by a number that is
allocated per country.

The exact format of the numbers varies per country and a country-specific
check is performed on the number using the VAT module that is relevant for
that country.

>>> compact('ATU 57194903')
'ATU57194903'
>>> validate('BE697449992')
'BE0697449992'
>>> validate('FR 61 954 506 077')
'FR61954506077'
>>> guess_country('00449544B01')
['nl']
"""

from stdnum.exceptions import *
from stdnum.util import clean


country_codes = set([
    'at', 'be', 'bg', 'cy', 'cz', 'de', 'dk', 'ee', 'es', 'fi', 'fr', 'gb',
    'gr', 'hr', 'hu', 'ie', 'it', 'lt', 'lu', 'lv', 'mt', 'nl', 'pl', 'pt', 'ro',
    'se', 'si', 'sk'
])
"""The collection of country codes that are queried. Greece is listed with
a country code of gr while for VAT purposes el is used instead."""

_country_modules = dict()

vies_wsdl = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'
"""The WSDL URL of the VAT Information Exchange System (VIES)."""

# a cached version of the suds client for VIES
_vies_client = None


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
    number = clean(number, '').upper().strip()
    module = _get_cc_module(number[:2])
    if not module:
        raise InvalidComponent()
    return number[:2] + module.compact(number[2:])


def validate(number):
    """Checks to see if the number provided is a valid VAT number. This
    performs the country-specific check for the number."""
    number = clean(number, '').upper().strip()
    module = _get_cc_module(number[:2])
    if not module:
        raise InvalidComponent()
    return number[:2] + module.validate(number[2:])


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    performs the country-specific check for the number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def guess_country(number):
    """Guess the country code based on the provided number. This checks the
    provided number against each of the validation routines and returns
    the list of countries for which it is valid. This returns lower case
    codes and returns gr (not el) for Greece."""
    return [cc
            for cc in country_codes
            if _get_cc_module(cc).is_valid(number)]


def check_vies(number):  # pragma: no cover (no tests for this function)
    """Queries the online European Commission VAT Information Exchange
    System (VIES) for validity of the provided number. Note that the
    service has usage limitations (see the VIES website for details).
    This returns a dict-like object."""
    # this function isn't automatically tested because it would require
    # network access for the tests and unnecessarily load the VIES website
    number = compact(number)
    global _vies_client
    if not _vies_client:
        from suds.client import Client
        try:
            from urllib import getproxies
        except ImportError:
            from urllib.request import getproxies
        _vies_client = Client(vies_wsdl, proxy=getproxies())
    return _vies_client.service.checkVat(number[:2], number[2:])
