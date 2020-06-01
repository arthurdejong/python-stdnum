# upn.py - functions for handling English UTRs
#
# Copyright (C) 2020 Holvi Payment Services
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

"""UTR (English Unique Tax Payer Reference).

The unique taxpayer reference (UTR). The format is a unique set of 10 numerals
allocated automatically by HMRC for both individuals and entities who have to
submit a tax return. Although used on tax returns and some other correspondence,
the UTR is not evidenced on a card or other official document. 


More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/UK-TIN.pdf

>>> validate('9999999999')
'9999999999'
>>> validate('12345678')
Traceback (most recent call last):
    ...
InvalidLength: ..
>>> validate('A12345678')
Traceback (most recent call last):
    ...
InvalidFormat: ..
"""
from stdnum.exceptions import *
from stdnum.util import isdigits


def validate(number):
    """
        Check if the number is a valid UTR.
        This checks thelength of the identifier.
    """
    if not isdigits(number):
        raise InvalidFormat()
    if not len(number) == 9:
        raise InvalidLength()


def is_valid(number):
    """Check if the number is a valid UTR."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
