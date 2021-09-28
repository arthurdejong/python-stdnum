# pan.py - functions for handling Indian Permanent Account number (PAN)
#
# Copyright (C) 2017 Srikanth Lakshmanan
# Copyright (C) 2021 Gaurav Chauhan
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

"""PAN (Permanent Account Number, Indian income tax identifier).

The Permanent Account Number (PAN) is a 10 digit alphanumeric identifier for
Indian individuals, families and corporates for income tax purposes.

PAN is made up of 5 letter, 4 digits and one alphabetic check digit. The
fourth character indicates the type of holder, the fifth character (of PAN)
is either first character of the holder's name or first character of surname
in case of 'personal' PAN, next four digits are serial numbers running from
0001 to 9999 and the last character is a check digit computed by an
undocumented checksum algorithm.

More information:

* https://en.wikipedia.org/wiki/Permanent_account_number
* https://incometaxindia.gov.in/tutorials/1.permanent%20account%20number%20(pan).pdf

>>> validate('ACUPA7085R')
'ACUPA7085R'
>>> validate('ACUPA7085RR')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('ACUPA70852')  # check digit should be a letter
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('ACUZA7085R')  # invalid type of holder
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> mask('ACUPA7085R')
'ACUPAXXXXR'
>>> info('ACUPA7085R')['card_holder_type']
'Individual'
"""

import re
import stdnum.exceptions as e

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').upper().strip()


def info(number):
    """Provide information that can be decoded from the PAN."""
    card_holder_types = {
        'A': 'Association of Persons (AOP)',
        'B': 'Body of Individuals (BOI)',
        'C': 'Company',
        'F': 'Firm/Limited Liability Partnership',
        'G': 'Government Agency',
        'H': 'Hindu Undivided Family (HUF)',
        'L': 'Local Authority',
        'J': 'Artificial Juridical Person',
        'P': 'Individual',
        'T': 'Trust',
    }
    number = compact(number)
    card_holder_type = card_holder_types.get(number[3])
    if not card_holder_type:
        raise e.InvalidComponent()
    return {
        'card_holder_type': card_holder_type,
        'initial': number[4],
    }


def validate(number):
    """Check if the number provided is a valid PAN. This checks the length
    and formatting."""
    pan_re = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]$')
    number = compact(number)
    if len(number) != 10:
        raise e.InvalidLength()
    if not pan_re.match(number):
        raise e.InvalidFormat()
    if int(number[5:9]) == 0:  # check serial number range
        raise e.InvalidFormat()
    info(number)  # check the fourth digit
    return number


def is_valid(number):
    """Check if the number provided is a valid PAN. This checks the length
    and formatting."""
    try:
        return bool(validate(number))
    except e.ValidationError:
        return False


def mask(number):
    """Mask the PAN as per Central Board of Direct Taxes (CBDT) masking
    standard."""
    number = compact(number)
    return number[:5] + 'XXXX' + number[-1:]
