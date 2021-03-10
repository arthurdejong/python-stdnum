# isrc.py - functions for International Standard Recording Codes (ISRC)
#
# Copyright (C) 2021 Nuno André Novo
# Copyright (C) 2014-2021 Arthur de Jong
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

"""ISRC (International Standard Recording Code).

The ISRC is an international standard code (ISO 3901) for uniquely
identifying sound recordings and music video recordings.

More information:

* https://en.wikipedia.org/wiki/International_Standard_Recording_Code
"""

from stdnum.exceptions import *
from stdnum.util import clean, segment
from stdnum.isin import _iso_3116_1_country_codes
from string import ascii_uppercase, digits


# These special codes are allowed for ISRC
_country_codes = set(_iso_3116_1_country_codes + [
    'QM',  # US new registrants due to US codes became exhausted
    'CP',  # reserved for further overflow
    'DG',  # idem
    'ZZ',  # International ISRC Agency codes
])

_chunks = 2, 3, 2, 5


def compact(number):
    """Convert the ISRC to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def validate(number):
    """Check if the number provided is a valid ISRC. This checks the length,
    the alphabet, and the country code but does not check if the registrant
    code is known."""
    number = compact(number)
    country, registrant, year, record = segment(number, *_chunks)

    if len(number) != 12:
        raise InvalidLength()
    if any(c not in ascii_uppercase + digits for c in registrant):
        raise InvalidFormat()
    if any(c not in digits for c in year + record):
        raise InvalidFormat()
    if country not in _country_codes:
        raise InvalidComponent()

    return number


def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number, separator='-'):
    """Reformat the number to the common representation."""
    parts = segment(compact(number), *_chunks)
    return separator.join(parts)
