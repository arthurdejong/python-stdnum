# uen.py - functions for handling Singapore UEN numbers
# coding: utf-8
#
# Copyright (C) 2020 Leandro Regueiro
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

"""UEN (Singapore's Unique Entity Number).

There are four different UEN numbers:

* UEN – Business (ROB): It has a total length of 9 characters. Consists
  of 8 digits followed by a check letter.
* UEN – Local Company (ROC): It has a total length of 10 characters.
  Consists of 9 digits (the 4 leftmost digits represent the year of
  issuance) followed by a check letter.
* UEN – Foreign Companies: It has a total length of 10 characters.
  Begins with the letter F, followed by either 3 zeroes or
  alternatively 3 whitespaces, then followed by 5 digits, and finally
  by a check letter.
* UEN – Others: It has a total length of 10 characters. Begins with
  either the R letter, or the S letter or the T letter (where R
  represents '18', S represents '19' and T represents '20') followed by
  2 digits representing the last two digits of the issuance year. After
  that come two letters representing the entity type, followed by 4
  digits, and finally by a check letter.

  For example 'T08' means year 2008, 'S99' means year 1999, and 'R00'
  means year 1800.

  Entity type must be one of the following:
    'CC', 'CD', 'CH', 'CL', 'CM', 'CP', 'CS', 'CX', 'DP', 'FB', 'FC',
    'FM', 'FN', 'GA', 'GB', 'GS', 'HS', 'LL', 'LP', 'MB', 'MC', 'MD',
    'MH', 'MM', 'MQ', 'NB', 'NR', 'PA', 'PB', 'PF', 'RF', 'RP', 'SM',
    'SS', 'TC', 'TU', 'VH', 'XL'.

  For example, the UEN for a limited liability partnership (LLP) formed
  on 1 January 2009 could be 'T09LL0001B'.

More information:

* https://www.oecd.org/tax/automatic-exchange/crs-implementation-and-assistance/tax-identification-numbers/Singapore-TIN.pdf
* https://www.uen.gov.sg/ueninternet/faces/pages/admin/aboutUEN.jspx

>>> validate('00192200M')
'00192200M'
>>> validate('197401143C')
'197401143C'
>>> validate('F00056789H')
'F00056789H'
>>> validate('F   56789H')
'F00056789H'
>>> validate('S16FC0121D')
'S16FC0121D'
>>> validate('T01FC6132D')
'T01FC6132D'
>>> validate('123456')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('F   56789H')
'F00056789H'
"""

from datetime import datetime

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


OTHER_UEN_ENTITY_TYPES = ('CC', 'CD', 'CH', 'CL', 'CM', 'CP', 'CS', 'CX',
                          'DP', 'FB', 'FC', 'FM', 'FN', 'GA', 'GB', 'GS',
                          'HS', 'LL', 'LP', 'MB', 'MC', 'MD', 'MH', 'MM',
                          'MQ', 'NB', 'NR', 'PA', 'PB', 'PF', 'RF', 'RP',
                          'SM', 'SS', 'TC', 'TU', 'VH', 'XL')


def compact(number):
    """Convert the number to the minimal representation.

    This converts to uppercase and removes surrounding whitespace. It
    also replaces the whitespace in UEN for foreign companies with
    zeroes.
    """
    return clean(number).upper().strip().replace(' ', '0')


def _validate_business_uen(number):
    """Perform validation on UEN – Business (ROB) numbers."""
    if not isdigits(number[:-1]):
        raise InvalidFormat()
    if not number[-1].isalpha():
        raise InvalidFormat()


def _validate_local_company_uen(number):
    """Perform validation on UEN – Local Company (ROC) numbers."""
    if not isdigits(number[:-1]):
        raise InvalidFormat()
    current_year = str(datetime.now().year)
    if number[:4] > current_year:
        raise InvalidComponent()
    if not number[-1].isalpha():
        raise InvalidFormat()


def _validate_foreign_companies_uen(number):
    """Perform validation on UEN – Foreign Companies numbers."""
    if number[1:4] not in ('000', '   '):
        raise InvalidComponent()
    if not isdigits(number[4:-1]):
        raise InvalidFormat()
    if not number[-1].isalpha():
        raise InvalidFormat()


def _validate_other_uen(number):
    """Perform validation on other UEN numbers."""
    if number[0] not in ('R', 'S', 'T'):
        raise InvalidComponent()
    if not isdigits(number[1:3]):
        raise InvalidFormat()
    current_year = str(datetime.now().year)
    if number[0] == 'T' and number[1:3] > current_year[2:]:
        raise InvalidComponent()
    if number[3:5] not in OTHER_UEN_ENTITY_TYPES:
        raise InvalidComponent()
    if not isdigits(number[5:-1]):
        raise InvalidFormat()
    if not number[-1].isalpha():
        raise InvalidFormat()


def validate(number):
    """Check if the number is a valid Singapore UEN number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) not in (9, 10):
        raise InvalidLength()
    # UEN – Business (ROB).
    if len(number) == 9:
        _validate_business_uen(number)
        return number
    # UEN – Local Company (ROC).
    if not number[0].isalpha():
        _validate_local_company_uen(number)
        return number
    # UEN – Foreign Companies.
    if number[0] == 'F':
        _validate_foreign_companies_uen(number)
        return number
    # UEN – Others.
    _validate_other_uen(number)
    return number


def is_valid(number):
    """Check if the number is a valid Singapore UEN number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)
