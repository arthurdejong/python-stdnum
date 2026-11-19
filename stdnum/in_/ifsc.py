# ifsc.py - functions for handling Indian IFSC bank branch codes
#
# Copyright (C) 2026 Yash Budhia
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

"""IFSC (Indian Financial System Code).

The Indian Financial System Code (IFSC) is an 11 character alphanumeric code
that the Reserve Bank of India (RBI) assigns to every bank branch that takes
part in the NEFT, RTGS and IMPS electronic funds transfer systems. It is
required for every domestic electronic transfer in India and is also used to
route UPI payments.

The code consists of a 4 letter bank code, a fifth character that is reserved
and always 0, and a 6 character branch code. The branch code is often numeric
but may contain letters, which is common for cooperative and other sub-member
banks that transact through a sponsor bank. There is no check digit.

More information:

* https://en.wikipedia.org/wiki/Indian_Financial_System_Code
* https://www.rbi.org.in/Scripts/IFSCMICRDetails.aspx
* https://github.com/razorpay/ifsc

>>> validate('SBIN0000001')
'SBIN0000001'
>>> validate('hdfc0cabblm')
'HDFC0CABBLM'
>>> validate('SBIN000001')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('SB1N0000001')  # bank code must be letters
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('SBIN1000001')  # fifth character is reserved and must be 0
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> info('ICIC0000001')['bank_code']
'ICIC'
"""

from __future__ import annotations

import re

from stdnum.exceptions import *
from stdnum.util import clean


_ifsc_re = re.compile(r'^[A-Z]{4}[A-Z0-9]{7}$')


def compact(number: str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def validate(number: str) -> str:
    """Check if the number provided is a valid IFSC. This checks the length
    and formatting."""
    number = compact(number)
    if len(number) != 11:
        raise InvalidLength()
    if not _ifsc_re.match(number):
        raise InvalidFormat()
    if number[4] != '0':
        raise InvalidComponent()
    return number


def is_valid(number: str) -> bool:
    """Check if the number provided is a valid IFSC. This checks the length
    and formatting."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def info(number: str) -> dict[str, str]:
    """Provide information that can be decoded from the IFSC."""
    number = compact(number)
    return {
        'bank_code': number[:4],
        'branch_code': number[5:],
    }
