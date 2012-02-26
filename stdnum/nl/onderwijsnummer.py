# onderwijsnummer.py - functions for handling onderwijsnummers
#
# Copyright (C) 2012 Arthur de Jong
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

"""Onderwijsnummer (Dutch school number).

The onderwijsnummers (school number) is very similar to the BSN (Dutch
national identification number) but for students without a BSN. It uses a
small variation of the BSN checksum.

>>> is_valid('101222331')
True
>>> is_valid('100252333')
False
>>> compact('1234.56.782')
'123456782'
"""

from stdnum.nl.bsn import compact, checksum


__all__ = ['compact', 'is_valid']


def is_valid(number):
    """Checks to see if the number provided is a valid onderwijsnummer.
    This checks the length and whether the check digit is correct and
    whether it starts with the right sequence."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 9 and \
           number.isdigit() and \
           int(number) > 0 and \
           checksum(number) == 5 and \
           number.startswith('10')
