# excise.py - functions for handling EU Excise numbers
# coding: utf-8
#
# Copyright (C) 2023 Cédric Krier
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

"""Excise Number

The Excise Number is the identification number issued by the competent
authority in respect of the person or premises. It is used to identify the
taxpayers of excise taxes.

The first two letters are the ISO country code of the Member State where the
operator is located (e.g. LU);
The next 11 alphanumeric characters are the identifier of the operator.
The identifier must include 11 digits, shorter identifiers must be padded to
the left with zeroes (e.g. 00000987ABC)

More information:

* https://ec.europa.eu/taxation_customs/dds2/seed/help/seedhedn.jsp

>>> compact('LU 00000987ABC')
'LU00000987ABC'
>>> validate('LU00000987ABC')
'LU00000987ABC'
"""

from stdnum.eu.vat import MEMBER_STATES
from stdnum.exceptions import *
from stdnum.util import clean, get_cc_module, get_soap_client


_country_modules = dict()

seed_wsdl = 'https://ec.europa.eu/taxation_customs/dds2/seed/services/excise/verification?wsdl'
"""The WSDL URL of the System for Exchange of Excise Data (SEED)."""


def _get_cc_module(cc):
    """Get the Excise number module based on the country code."""
    cc = cc.lower()
    if cc not in MEMBER_STATES:
        raise InvalidComponent()
    if cc not in _country_modules:
        _country_modules[cc] = get_cc_module(cc, 'excise')
    return _country_modules[cc]


def compact(number):
    """Convert the number to the minimal representation. This strips the number
    of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' ').upper().strip()
    return number


def validate(number):
    """Check if the number is a valid Excise number."""
    number = clean(number, ' ').upper().strip()
    cc = number[:2]
    if len(number) != 13:
        raise InvalidLength()
    module = _get_cc_module(cc)
    if module:
        module.validate(number)
    return number


def is_valid(number):
    """Check if the number is a valid Excise number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def check_seed(number, timeout=30):  # pragma: no cover (not part of normal test suite)
    """Query the online European Commission System for Exchange of Excise Data
    (SEED) for validity of the provided number. Note that the service has
    usage limitations (see the VIES website for details). The timeout is in
    seconds. This returns a dict-like object."""
    number = compact(number)
    client = get_soap_client(seed_wsdl, timeout)
    return client.verifyExcise(number)
