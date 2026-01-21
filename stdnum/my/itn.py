# itn.py - functions for handling ITN numbers
#
# Copyright (C) 2020 Sergi Almacellas Abellana
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

"""ITN No. (Malaysian Income Tax Number)

The number is assigned by The Inland Revenue Board of Malaysia (IRBM) and it
is required to report the income. This unique number is known as
"Nombor CukaiPendapatan" or Income Tax Number.

The number consist of 11 or 12 digits. It is structured by two types, normally
separated by an space. The first one consists of 1 or 2 leters and represents
the type of the file number. The second one is always ten digits an represents
the tax number.

>>> validate('C2584563202')
'C2584563202'
>>> validate('CDB2584563202')  # Should contain the prefix
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('CD12346789012')  # Should contain the prefix
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('C258456320B')  # number should only contain digits
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> format('C2584563202')
'C 2584563202'
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -*').strip()


def split(number):
    number = compact(number)
    index = 10
    if len(number) > 12:
        index += 11
    return number[:-index], number[-index:]


def validate(number):
    """Check if the number is a valid NRIC number. This checks the length,
    formatting and birth date and place."""
    number = compact(number)
    if len(number) > 13 or len(number) <= 10:
        raise InvalidLength()
    prefix, digits = split(number)
    if not prefix or len(prefix) > 2:
        raise InvalidLength()
    if not isdigits(digits):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number is a valid NRIC number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return ' '.join(split(number))
