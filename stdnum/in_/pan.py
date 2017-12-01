# pan.py - functions for handling Indian Permanent Account number (PAN)
#
# Copyright (C) 2017 Srikanth Lakshmanan
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

"""PAN (Permanent Account Number - Indian income tax identifier).
https://en.wikipedia.org/wiki/Permanent_account_number#Structure_and_provisions

The PAN is a 10 digit alphanumeric number of the following structure.
The first 3 digits - Alphabetic sequence AAA-ZZZ
The forth digit indicates type of holder
The next 4 digits will be sequential number 0001-9999
The last digit will be for check code. It is an alphabet computed by an undocumented checksum algorithm

>>> is_valid('AAPPV8261K')  #Valid PAN
True

>>> is_valid('ABMPA3211G')  #Valid PAN
True

>>> validate('ACUPA7085R')  #Valid PAN
'ACUPA7085R'

>>> validate('234123412347')  # 12 digit non-1 starting invalid checksum (incorrect check)
Traceback (most recent call last):
    ...
InvalidFormat: ...

>>> validate('ABMPA32111')  # Check digit ending in number (incorrect check)
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('ABMXA3211G')  # Invalid type of holder (incorrect check)
Traceback (most recent call last):
    ...
InvalidFormat: ...

>>> mask('AAPPV8261K')
'AAPPVXXXXK'

>>> mask('ABMPA32111')
'Invalid PAN'
"""

import re

from stdnum.exceptions import *
from stdnum.util import clean


pan_re = re.compile(r'^[A-Z]{3}[ABCFGHLJPTK][A-Z]\d{4}[A-Z]$')
"""Regular expression used to check structure of PAN."""


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def validate(number):
    """Check if the number provided is a valid PAN. This checks the
    length, formatting."""
    number = compact(number)
    if len(number) != 10:
        raise InvalidLength()
    if not pan_re.match(number):
        raise InvalidFormat()
    return number


def is_valid(number):
    """Check if the number provided is a valid PAN number. This checks the
    length, formatting."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def info(number):
    """Provides information that can be decoded from the PAN"""
    type_of_card_holder = {
        'A': 'Association of Persons (AOP)',
        'B': 'Body of Individuals (BOI)',
        'C': 'Company',
        'F': 'Firm',
        'G': 'Government',
        'H': 'HUF (Hindu Undivided Family)',
        'L': 'Local Authority',
        'J': 'Artificial Juridical Person',
        'P': 'Individual',
        'T': 'Trust(AOP)',
        'K': 'Krish (Trust Krish)'}
    info_str = "Card holder is " + type_of_card_holder[number[3]]
    if number[3] == 'P':
        info_str = info_str + " whose surname / lastname"
    else:
        info_str = info_str + "whose name"
    info_str = info_str + " starts with character " + number[4]
    return info_str

def format(number):
    """Reformat the number to the standard presentation format."""
    return compact(number)

def mask(number):
    """Masks PAN as per CBDT masking standard"""
    number = compact(number)
    if is_valid(number):
        return number.replace(number[5:][:-1],'XXXX')
    else:
        return "Invalid PAN"