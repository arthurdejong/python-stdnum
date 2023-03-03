# cnp.py - functions for handling Romanian CNP numbers
# coding: utf-8
#
# Copyright (C) 2012-2020 Arthur de Jong
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

"""CNP (Cod Numeric Personal, Romanian Numerical Personal Code).

The CNP is a 13 digit number that includes information on the person's
gender, birth date and country zone.

More information:

* https://ro.wikipedia.org/wiki/Cod_numeric_personal

>>> validate('1630615123457')
'1630615123457'
>>> validate('0800101221142')  # invalid first digit
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('1632215123457')  # invalid date
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('1630615123458')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

import datetime

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def calc_check_digit(number):
    """Calculate the check digit for personal codes."""
    # note that this algorithm has not been confirmed by an independent source
    weights = (2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9)
    check = sum(w * int(n) for w, n in zip(weights, number)) % 11
    return '1' if check == 10 else str(check)


def get_birth_date(number):
    """Split the date parts from the number and return the birth date."""
    number = compact(number)
    centuries = {
        '1': 1900, '2': 1900, '3': 1800, '4': 1800, '5': 2000, '6': 2000,
    }  # we assume 1900 for the others in order to try to construct a date
    year = int(number[1:3]) + centuries.get(number[0], 1900)
    month = int(number[3:5])
    day = int(number[5:7])
    try:
        return datetime.date(year, month, day)
    except ValueError:
        raise InvalidComponent()


def validate(number):
    """Check if the number is a valid VAT number. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    # first digit should be a known one
    # (7,8=foreign resident, 9=other foreigner but apparently only as NIF)
    if number[0] not in '123456789':
        raise InvalidComponent()
    if len(number) != 13:
        raise InvalidLength()
    # check if birth date is valid
    get_birth_date(number)
    # TODO: check that the birth date is not in the future
    # number[7:9] is the county, we ignore it for now, just check last digit
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid VAT number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False

def get_county(number):
    """Return county"""
    number=compact(number)
    counties= {
              '01':'Alba',
              '02':'Arad',
              '03':'Argeș',
              '04':'Bacău',
              '05':'Bihor',
              '06':'Bistrița-Năsăud',
              '07':'Botoșani',
              '08':'Brașov',
              '09':'Brăila',
              '10':'Buzău',
              '11':'Caraș-Severin',
              '12':'Cluj',
              '13':'Constanța',
              '14':'Covasna',
              '15':'Dâmbovița',
              '16':'Dolj',
              '17':'Galați',
              '18':'Gorj',
              '19':'Harghita',
              '20':'Hunedoara',
              '21':'Ialomița',
              '22':'Iași',
              '23':'Ilfov',
              '24':'Maramureș',
              '25':'Mehedinți',
              '26':'Mureș',
              '27':'Neamț',
              '28':'Olt',
              '29':'Prahova',
              '30':'Satu Mare',
              '31':'Sălaj',
              '32':'Sibiu',
              '33':'Suceava',
              '34':'Teleorman',
              '35':'Timiș',
              '36':'Tulcea',
              '37':'Vaslui',
              '38':'Vâlcea',
              '39':'Vrancea',
              '40':'București',
              '41':'București - Sector 1',
              '42':'București - Sector 2',
              '43':'București - Sector 3',
              '44':'București - Sector 4',
              '45':'București - Sector 5',
              '46':'București - Sector 6',
              '51':'Călărași',
              '52':'Giurgiu',
              '47':'Bucuresti - Sector 7 (desfiintat)',
              '48':'Bucuresti - Sector 8 (desfiintat)'
              }
    county=counties.get(number[7:9],'Alba')
    return county