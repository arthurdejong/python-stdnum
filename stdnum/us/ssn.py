# ssn.py - functions for handling SSNs
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

"""SSN (U.S. Social Security Number).

The Social Security Number is used to identify individuals for taxation
purposes.

>>> is_valid('111-22-3333')
True
>>> is_valid('1112-23333')
False
>>> is_valid('666-00-0000')
False
>>> compact('1234-56-789')
'123456789'
>>> format('111223333')
'111-22-3333'
"""

import re

from stdnum.util import clean


# regular expression for matching SSN
_ssn_re = re.compile('^(?P<area>[0-9]{3})-?(?P<group>[0-9]{2})-?(?P<serial>[0-9]{4})$')

# blacklist of SSNs
_ssn_blacklist = set(('078-05-1120', '457-55-5462', '219-09-9999'))


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '-').strip()


def is_valid(number):
    """Checks to see if the number provided is a valid SSN. This checks
    the length, groups and formatting if it is present."""
    try:
        match = _ssn_re.search(number.strip())
    except:
        return False
    if not match:
        return False
    area = match.group('area')
    group = match.group('group')
    serial = match.group('serial')
    # check for all-0 or some unused areas
    # (9xx also won't be issued which includes the advertising range)
    if area == '000' or area == '666' or area[0] == '9' or \
       group == '00' or serial == '0000':
        return False
    # check blacklists
    return format(number) not in _ssn_blacklist


def format(number):
    """Reformat the passed number to the standard format."""
    if len(number) == 9:
        number = number[:3] + '-' + number[3:5] + '-' + number[5:]
    return number
