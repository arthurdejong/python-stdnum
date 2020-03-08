# vatin.py - function to validate any given VATIN.
#
# Copyright (C) 2020 Leandro Regueiro
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

"""Check whether a given VAT identification number is valid.

>>> check_vatin('FR 40 303 265 045')
True
>>> check_vatin('DE136,695 976')
True
>>> check_vatin('BR16.727.230/0001-97')
True
>>> check_vatin('FR 40 303')
False
>>> check_vatin('')
False
>>> check_vatin('XX')
Traceback (most recent call last):
    ...
MissingValidation: ...
>>> check_vatin('US')
Traceback (most recent call last):
    ...
MissingValidation: ...
"""

import importlib


class MissingValidation(Exception):
    """Missing validation.

    Either there is no module for the country, or country has no module
    to perform validation.
    """

    def __str__(self):
        """Return the exception message."""
        return 'Unable to locate code to perform validation.'


def check_vatin(vatin):
    """Check whether a given VAT identification number is valid.

    A value added tax identification number or VAT identification
    number (VATIN) is an identifier used in many countries, including
    the countries of the European Union, for value added tax purposes.

    VATIN starts with an ISO 3166-1 alpha-2 (2 letters) country code
    (except for Greece, which uses EL, instead of GR) and then it comes
    the identifier.

    Identifiers are composed of numeric digits in most countries, but
    in some countries they may contain letters and other characters
    like dots, hyphens, slashes and whitespaces. They have different
    lengths and formats depending on the country. Usually a check digit
    or letter is included which prevents it from being mistyped.

    Foreign companies that trade with non-enterprises in the EU may
    have a VATIN starting with "EU" instead of a country code, e.g.
    Godaddy USA EU826010755 and Amazon USA AWS EU826009064.

    https://en.wikipedia.org/wiki/VAT_identification_number
    """
    country_code = vatin[:2].lower()
    if not country_code:
        return False
    try:
        country_module = importlib.import_module('stdnum.' + country_code)
    except ImportError:
        raise MissingValidation
    try:
        return country_module.vat.is_valid(vatin[2:])
    except AttributeError:
        raise MissingValidation
