# upi.py - functions for handling Unique Product Identifiers (UPIs)
#
# Copyright (C) 2026 Jon Arnfred
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
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

"""UPI (ISO 4914 Unique Product Identifier).

The Unique Product Identifier (UPI) is a 12-character alphanumeric code used
to identify over-the-counter (OTC) derivative products. It consists of the
two-character prefix ``QZ``, nine characters that identify the product, and
one check character. Vowels and the letter Y are not used. The check
character uses the ISO 7064 Mod 31, 30 algorithm.

More information:

* https://www.iso.org/standard/80506.html
* https://www.anna-dsb.com/upi-/
* https://zakon.rada.gov.ua/laws/show/z1549-21

>>> validate('QZK12RNSP6P6')
'QZK12RNSP6P6'
>>> validate('QZK12RNSP6P7')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> calc_check_digit('QZK12RNSP6P')
'6'
"""

from __future__ import annotations

from stdnum.exceptions import *
from stdnum.iso7064 import mod_37_36
from stdnum.util import clean


# The UPI alphabet excludes vowels and the letter Y. Using this alphabet with
# the generic Mod x+1, x implementation gives the ISO 7064 Mod 31, 30 method.
_alphabet = '0123456789BCDFGHJKLMNPQRSTVWXZ'


def compact(number: str) -> str:
    """Convert the UPI to its minimal representation. This strips spaces and
    removes surrounding whitespace."""
    return clean(number, ' ').strip().upper()


def calc_check_digit(number: str) -> str:
    """Calculate the check character for the number."""
    return mod_37_36.calc_check_digit(compact(number), alphabet=_alphabet)


def validate(number: str) -> str:
    """Check if the number provided is a valid UPI. This checks the length,
    format, prefix and check character."""
    number = compact(number)
    if not all(x in _alphabet for x in number):
        raise InvalidFormat()
    if len(number) != 12:
        raise InvalidLength()
    if not number.startswith('QZ'):
        raise InvalidComponent()
    mod_37_36.validate(number, alphabet=_alphabet)
    return number


def is_valid(number: str) -> bool:
    """Check if the number provided is a valid UPI."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
