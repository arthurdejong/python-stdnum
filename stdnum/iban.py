# iban.py - functions for handling International Bank Account Numbers (IBANs)
#
# Copyright (C) 2011, 2012 Arthur de Jong
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

"""IBAN (International Bank Account Number).

The IBAN is used to identify bank accounts across national borders. The
first two letters are a country code. The next two digits are check digits
for the ISO 7064 Mod 97, 10 checksum. Each country uses it's own format
for the remainder of the number.

Some countries may also use checksum algorithms within their number but
this is currently not checked by this number.

>>> is_valid('GR16 0110 1050 0000 1054 7023 795')
True
>>> is_valid('BE31435411161155')
True
>>> compact('GR16 0110 1050 0000 1054 7023 795')
'GR1601101050000010547023795'
>>> format('GR1601101050000010547023795')
'GR16 0110 1050 0000 1054 7023 795'
"""

import re

from stdnum import numdb
from stdnum.iso7064 import mod_97_10
from stdnum.util import clean


# our open copy of the IBAN database
_ibandb = numdb.get('iban')

# the valid characters we have
_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# regular expression to check IBAN structure
_struct_re = re.compile('([1-9][0-9]*)!([nac])')


def compact(number):
    """Convert the iban number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def _convert(number):
    """Prepare the number to it's base10 representation (also moving the
    check digits to the end) so it can be checked with the ISO 7064
    Mod 97, 10 algorithm."""
    # TODO: find out whether this should be in the mod_97_10 module
    return ''.join(str(_alphabet.index(x)) for x in number[4:] + number[:4])


def _matches_structure(number, structure):
    """Check the supplied number against the supplied structure."""
    start = 0
    for length, code in _struct_re.findall(structure):
        length = int(length)
        if code == 'n' and not number[start:start + length].isdigit():
            return False
        elif code == 'a' and not number[start:start + length].isalpha():
            return False
        elif code == 'c' and not number[start:start + length].isalnum():
            return False  # pragma: no cover (due to checksum check)
        start += length
    # the whole number should be parsed now
    return start == len(number)


def is_valid(number):
    """Checks to see if the number provided is a valid IBAN."""
    try:
        number = compact(number)
        # ensure that checksum is valid
        if not mod_97_10.is_valid(_convert(number)):
            return False
    except:
        return False
    # look up the number
    info = _ibandb.info(number)
    # check if the number has the correct structure
    return _matches_structure(number[4:], info[0][1].get('bban', ''))


def format(number, separator=' '):
    """Reformat the passed number to the space-separated format."""
    number = compact(number)
    return separator.join(number[i:i + 4] for i in range(0, len(number), 4))
