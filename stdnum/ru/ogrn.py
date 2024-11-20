
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
>>> validate('1022500001325')
True
>>> validate('10277395526422') # 14 digits
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('1022500001328') # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

import re
from typing import Optional

from stdnum.exceptions import *


def validate(text: str) -> bool:
    """Determine if the given string is a valid OGRN."""
    if not isinstance(text, str) or text is None:
        raise TypeError("Expected a string or bytes-like object, got '{}'"
                        .format(type(text).__name__))
    if len(text) not in {13, 15} or not text.isdigit():
        raise InvalidLength()
    if text[0] == '0':
        raise InvalidComponent()
    federal_subject_code = int(text[3:5])
    if federal_subject_code not in set(range(1, 80)) | {83, 86, 87, 89, 91, 92, 99}:
        raise InvalidComponent()
    control_digit = int(text[-1])
    if control_digit != calculate_control_digit(text):
        raise InvalidChecksum()
    return True

def format(text: str) -> Optional[str]:
    """Normalize the given string to a valid OGRN."""
    if not isinstance(text, str):
        return None
    match = re.compile(r'\b(\d{13}|\d{15})\b').search(text)
    if match is None:
        raise InvalidLength()
    return match.group(1)


def calculate_control_digit(grn: str) -> Optional[int]:
    """Calculate the control digit of the OGRN based on its length."""
    if len(grn) == 13:
        number = int(grn[:12])
        mod_result = number % 11
        calculated_digit = mod_result if mod_result != 10 else 0
        return calculated_digit
    elif len(grn) == 15:
        number = int(grn[:14])
        mod_result = number % 13
        calculated_digit = mod_result if mod_result != 10 else 0
        return calculated_digit
    return None


def is_valid(text: str) -> bool:
    """Check if the number is a valid OGRN."""
    try:
        normalized_text = format(text)
        return bool(normalized_text and validate(normalized_text))
    except ValidationError:
        return False