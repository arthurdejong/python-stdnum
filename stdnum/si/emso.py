# emso.py - functions for handling Slovenian Unique Master Citizen Numbers
# coding: utf-8
#
# Copyright (C) 2022 Blaž Bregar
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

"""Enotna matična številka občana (Unique Master Citizen Number).

The EMŠO is used for uniquely identify each physical person, it is perscribed
by Centralni Register Prebivalstva CRP (Central Citizen Registry), including
foreign citizens living in Slovenia.
https://sl.wikipedia.org/wiki/Enotna_mati%C4%8Dna_%C5%A1tevilka_ob%C4%8Dana
https://en.wikipedia.org/wiki/Unique_Master_Citizen_Number

EMŠO contains some personal data, namely date of brith and gender.

It is composed of 13 digits in the following pattern:
DDMMYYY RR BBBK

1. Date of birth (DDMMYYY)
  Date of birth with 3 digit year (skipping the milenia number)
  i.e. January first 2006 respresented as: 0101006
  Since EMŠO was implemented in 1977, YYY less than 800 will be considered
  in 3rd century (after year 2000), those higher or equal to 800 will be
  considered in 2nd century (before year 2000).

2. Political region (RR)
  Slovenia - 50-59 reserved (only 50 used)

3. Unique number of the particular RR (BBB)
  - 000-499 - Male
  - 500-999 - Female

4. Checksum (K)
  The checksum is calculated from the mapping DDMMYYYRRBBBK = abcdefghijklm, using the formula:

    m = 11 − (( 7×(a + g) + 6×(b + h) + 5×(c + i) + 4×(d + j) + 3×(e + k) + 2×(f + l) ) mod 11)

    - If m is between 1 and 9, the number K is the same as the number m
    - If m is 10 or 11 K becomes 0 (zero)
    Source: Wikipedia - https://en.wikipedia.org/wiki/Unique_Master_Citizen_Number



>>> validate('0101006500006')
'0101006500006'
>>> validate('0101006500007')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""
import datetime

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def calc_check_digit(number):
    """Calculate the check digit."""
    emso_factor_map = [7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    def emso_digit(number, place):
        try:
            return int(str(number)[place])
        except IndexError:
            raise InvalidFormat()

    emso_sum = 0
    for digit in range(12):
        emso_sum += emso_digit(number, digit) * emso_factor_map[digit]
    control_digit = 11 - (emso_sum % 11)

    if control_digit == 11:
        control_digit = 0

    return str(control_digit)


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace.
    Removes SI prefix, as it is used as ID za DDV (VAT identifier)."""
    number = clean(number, ' ').strip()
    return number


def get_date(number):
    """Return date of birth from valid EMŠO."""
    day = int(str(number)[:2])
    month = int(str(number)[2:4])
    year = str(number)[4:7]
    if int(year[0]) < 8:
        year = '2' + year
    else:
        year = '1' + year
    try:
        dob = datetime.date(int(year), month, day)
    except ValueError:
        raise InvalidFormat()
    return dob


def get_gender(number):
    """Return gender from valid EMŠO.
    M - represents male
    F - represents female"""
    bbb = number[9:12]
    try:
        bbb = int(bbb)
    except ValueError:
        raise InvalidFormat()
    if bbb < 500:
        return 'M'
    else:
        return 'F'


def get_region(number):
    """Return (political) region from valid EMŠO.
    Source: Wikipedia - https://en.wikipedia.org/wiki/Unique_Master_Citizen_Number
    For details look at emso_rr
    """
    return number[7:9]


def validate(number):
    """Check if the number is a valid EMŠO number. This checks the length,
    formatting and check digit."""
    number = compact(number)
    # Check length
    if len(number) != 13:
        raise InvalidLength()
    # Check if only digits
    if not isdigits(number):
        raise InvalidFormat()
    # Check date of brith
    if not get_date(number):
        raise InvalidFormat()
    # Check checksum
    if calc_check_digit(number) != number[-1]:
        raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number provided is a valid ID. This checks the length,
    formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def extract(number):
    """Extract data from a valid EMŠO."""
    number = validate(number)
    return (number, get_date(number), get_region(number), get_gender(number))

def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
