# onrc.py - functions for handling Romanian ONRC numbers
# coding: utf-8
#
# Copyright (C) 2024 Dimitrios Josef Moustos
# Copyright (C) 2020 Arthur de Jong
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

"""ONRC (Ordine din Registrul Comer\xc5\xa3ului, Romanian Trade Register identifier).

All businesses in Romania have the to register with the National Trade
Register Office to receive a registration number. The number contains
information about the type of company, registration year, a sequence number,
county and a control sum.
On 2024-07-26 a new format was introduced and for a while both old and new
formats need to be valid.

>>> validate('J52/750/2012')
'J52/750/2012'
>>> validate('X52/750/2012')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('J2012000750528')
'J2012000750528'
"""

import datetime
import re

from stdnum.exceptions import *
from stdnum.util import clean


# These characters should all be replaced by slashes
_cleanup_re = re.compile(r'[ /\\-]+')

# This pattern should match numbers that for some reason have a full date
# as last field for the old format
_old_onrc_fulldate_re = re.compile(r'^([A-Z][0-9]+/[0-9]+/)\d{2}[.]\d{2}[.](\d{4})$')

# This pattern should match all valid old format numbers
_old_onrc_re = re.compile(r'^[A-Z][0-9]+/[0-9]+/[0-9]+$')

# This pattern should match all valid new format numbers
_onrc_re = re.compile(r'^[A-Z]\d{4}\d{6}\d{2}\d$')


# List of valid counties
_counties = set(list(range(1, 41)) + [51, 52])

# Calculate the control digit which is used in the last position of the new format
def _calculate_control_digit(number):
    """Calculate the control digit for the new ONRC format."""
    values = {'J': 10, 'F': 6, 'C': 3}
    num = number[:-1]  # Exclude control digit
    total = values.get(num[0], 0)  # Map letter to value
    total += sum(int(d) for d in num[1:] if d.isdigit())
    return (total + 4) % 10

# This function is only necessary for the old format
def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = _cleanup_re.sub('/', clean(number).upper().strip())
    # remove optional slash between first letter and county digits
    if number[1:2] == '/':
        number = number[:1] + number[2:]
    # normalise county number to two digits
    if number[2:3] == '/':
        number = number[:1] + '0' + number[1:]
    # convert trailing full date to year only
    m = _old_onrc_fulldate_re.match(number)
    if m:
        number = ''.join(m.groups())
    return number


def validate(number):
    """Check if the number is a valid ONRC."""
    if _onrc_re.match(number):
        if number[0] not in 'JFC':
            raise InvalidComponent("Invalid register type. Must be J, F, or C.")
        year = int(number[1:5])
        sequence = number[5:11]
        county = int(number[11:13])
        control_digit = int(number[13])

        # Validate year
        if year < 1990 or year > datetime.date.today().year:
            raise InvalidComponent("Year out of valid range.")

        # Validate sequence number (6 digits)
        if len(sequence) != 6 or not sequence.isdigit():
            raise InvalidLength("Sequence number must be exactly 6 digits.")

        # Companies registered before 2024-07-26 have the county code
        if (year <= 2024) and (county not in _counties):
            raise InvalidComponent("Invalid county code.")
        # Companies registered after 2024-07-26 have 00 as county code.
        if (year >= 2024) and (county == 0):
            raise InvalidComponent("Invalid county code.")

        # Validate control digit
        expected_control = _calculate_control_digit(number)
        if control_digit != expected_control:
            raise InvalidChecksum(f"Control digit {control_digit} does not match expected {expected_control}.")

        return number

    elif _old_onrc_re.match(number):
        number = compact(number)
        if number[:1] not in 'JFC':
            raise InvalidComponent()
        county, serial, year = number[1:].split('/')
        if len(serial) > 5:
            raise InvalidLength()
        if len(county) not in (1, 2) or int(county) not in _counties:
            raise InvalidComponent()
        if len(year) != 4:
            raise InvalidLength()
        if int(year) < 1990 or int(year) > 2024:
            raise InvalidComponent()
        return number
    else:
        raise InvalidFormat()


def is_valid(number):
    """Check if the number is a valid ONRC."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
