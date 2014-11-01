# iban.py - functions for handling International Bank Account Numbers (IBANs)
#
# Copyright (C) 2011, 2012, 2013 Arthur de Jong
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
for the ISO 7064 Mod 97, 10 checksum. Each country uses its own format
for the remainder of the number.

Some countries may also use checksum algorithms within their number but
this is currently not checked by this number.

>>> validate('GR16 0110 1050 0000 1054 7023 795')
'GR1601101050000010547023795'
>>> validate('BE31435411161155')
'BE31435411161155'
>>> compact('GR16 0110 1050 0000 1054 7023 795')
'GR1601101050000010547023795'
>>> format('GR1601101050000010547023795')
'GR16 0110 1050 0000 1054 7023 795'
"""

import re

from stdnum import numdb
from stdnum.exceptions import *
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


def _to_base10(number):
    """Prepare the number to its base10 representation (also moving the
    check digits to the end) so it can be checked with the ISO 7064
    Mod 97, 10 algorithm."""
    # TODO: find out whether this should be in the mod_97_10 module
    return ''.join(str(_alphabet.index(x)) for x in number[4:] + number[:4])


def _struct_to_re(structure):
    """Convert an IBAN structure to a refular expression that can be used
    to validate the number."""
    def conv(match):
        chars = {
            'n': '[0-9]',
            'a': '[A-Z]',
            'c': '[A-Za-z0-9]',
        }[match.group(2)]
        return '%s{%s}' % (chars, match.group(1))
    return re.compile('^%s$' % _struct_re.sub(conv, structure))


def validate(number):
    """Checks to see if the number provided is a valid IBAN."""
    number = compact(number)
    try:
        test_number = _to_base10(number)
    except Exception:
        raise InvalidFormat()
    # ensure that checksum is valid
    mod_97_10.validate(test_number)
    # look up the number
    info = _ibandb.info(number)
    # check if the bban part of number has the correct structure
    bban = number[4:]
    if not _struct_to_re(info[0][1].get('bban', '')).match(bban):
        raise InvalidFormat()
    # return the compact representation
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid IBAN."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number, separator=' '):
    """Reformat the passed number to the space-separated format."""
    number = compact(number)
    return separator.join(number[i:i + 4] for i in range(0, len(number), 4))
