# cas.py - functions for handling CAS registry numbers
#
# Copyright (C) 2022 Arthur de Jong
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

"""CAS Registry Number.

A CAS Registry Number, CAS RN or CAS number is a unique identified assign to
chemical substances. The number is issued by the Chemical Abstracts Service
(CAS).

The number consists of 5 to 10 digits and is assigned sequentially and
contains a check digit.

More information:

* https://en.wikipedia.org/wiki/CAS_Registry_Number
* https://www.cas.org/cas-data/cas-registry

>>> validate('12770-26-2')
'12770-26-2'
>>> validate('12770-29-2')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('012770-26-2')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


_cas_re = re.compile(r'^[1-9][0-9]{1,6}-[0-9]{2}-[0-9]$')


def compact(number):
    """Convert the number to the minimal representation."""
    return clean(number).strip()


def calc_check_digit(number):
    """Calculate the check digit. The number passed should not have the check
    digit included."""
    number = clean(number, '-').strip()
    return str(sum((i + 1) * int(n) for i, n in enumerate(reversed(number))) % 10)


def validate(number):
    """Check if the number is a valid CAS Registry Number."""
    number = compact(number)
    if not _cas_re.match(number):
        raise InvalidFormat()
    if not number[-1] == calc_check_digit(number[:-1]):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid CAS Registry Number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
