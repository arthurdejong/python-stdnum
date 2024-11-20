
# ogrn.py - functions for handling Russian company registration numbers
# coding: utf-8
#
# Copyright (C) 2010-2024 Arthur de Jong and others
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

"""ОГРН (Основной государственный регистрационный номер, Primary State Registration Number).

The OGRN is a Russian  identifier for legal entities that consists of either 13 or 15 digits.

>>> validate('1022200525819')
True
>>> validate('1027739') # too short
False
>>> validate('1022500001325')
True
>>> validate('10277395526422') # 14 digits
False
"""

import re
from typing import Optional

# Regular expression to match valid OGRN, which is either 13 or 15 digits.
OGRN_RE = re.compile(r'\b(\d{13}|\d{15})\b')

# Valid set of federal subject codes.
VALID_FEDERAL_SUBJECT_CODES = set(range(1, 80)) | {83, 86, 87, 89, 91, 92, 99}

# cf. https://docs.trellix.com/de-DE/bundle/data-loss-prevention-11.10.x-classification-definitions-reference-guide/page/GUID-945B4343-861E-4A57-8E60-8B6028871BA1.html


def is_valid(text: str) -> bool:
    """Determine if the given string is a valid OGRN."""
    if OGRN_RE.match(text) is None:
        return False

    # # Validate registration type, ensuring the first digit is not zero.
    if text[0] == '0':
        return False

    # Validate the federal subject code is within the allowable range.
    federal_subject_code = int(text[3:5])
    if federal_subject_code not in VALID_FEDERAL_SUBJECT_CODES:
        return False

    # Validate control digit logic
    control_digit = int(text[-1])
    return control_digit == calculate_control_digit(text)


def format(text: str) -> Optional[str]:
    """Normalize the given string to a valid OGRN."""
    match = OGRN_RE.search(text)
    if match is None:
        return None
    return match.group(1)


def calculate_control_digit(grn: str) -> Optional[int]:
    """Calculate the control digit of the OGRN based on its length."""
    if len(grn) == 13:
        number = int(grn[:12])
        mod_result = number % 11
        # Return the modulus result, or 0 if it results in 10.
        calculated_digit = mod_result if mod_result != 10 else 0
        return calculated_digit
    elif len(grn) == 15:
        number = int(grn[:14])
        mod_result = number % 13
        # Return the modulus result, or 0 if it results in 10.
        calculated_digit = mod_result if mod_result != 10 else 0
        return calculated_digit
    return None

def validate(text: str) -> bool:
    """Check if the number is a valid OGRN."""
    normalized_text = format(text)
    if normalized_text is None:
        return False
    return is_valid(normalized_text)

