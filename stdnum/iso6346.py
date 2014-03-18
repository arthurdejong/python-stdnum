# iso6346.py - functions for handling ISO 6346
#
# Copyright (C) 2014 Openlabs Technologies & Consulting (P) Limited
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
"""
ISO 6346
~~~~~~~~

ISO 6346 is an international standard covering the coding, identification and
marking of intermodal (shipping) containers used within containerized
intermodal freight transport. The standard establishes a visual identification
system for every container that includes a unique serial number (with check
digit), the owner, a country code, a size, type and equipment category as well
as any operational marks. The standard is managed by the International
Container Bureau (BIC).
"""
import re
import string

from stdnum.exceptions import InvalidChecksum, InvalidFormat, InvalidLength, \
    ValidationError


def _equivalent_number(character):
    """
    An equivalent numerical value is assigned to each letter of the alphabet,
    beginning with 10 for the letter A (11 and multiples thereof are omitted)
    """
    # 26 numbers starting at 10, excluding multipes of 11
    numbers = list(set(range(10, 39)) - set([11, 22, 33]))
    position = string.ascii_uppercase.index(character.upper())
    return numbers[position]


def calculate_check_digit(number):
    """
    Calculate check digit and return it for the 10 digit owner code and
    serial number
    """
    # Convert the number to upper case first
    number = number.upper()

    # Ensure this is a valid number, but without checksum
    if len(number) != 10:
        raise InvalidLength()

    if not re.match('^\w{3}(U|J|Z|R)\d{6}$', number):
        raise InvalidFormat()

    # Find the numbers (with equivalents) that make up the number
    result = map(
        int, map(_equivalent_number, number[:4]) + list(number[4:])
    )

    # Calculation Step 2: Each of the numbers calculated in step 1 is
    # multiplied by 2^position
    result = map(
        lambda num: pow(2, num[0]) * num[1],
        enumerate(result)
    )

    # Calculation Step 3: Calculate the remainder when the sum of the
    # above result is divided by 11
    return sum(result) % 11


def validate(number):
    """
    Validate the given number (unicode) for conformity to ISO 6346
    """
    if not number:
        raise InvalidFormat()
    number = unicode(number).upper()
    if len(number) != 11:
        raise InvalidLength()
    if not re.match('^\w{3}(U|J|Z|R)\d{7}$', number):
        raise InvalidFormat()
    if calculate_check_digit(number[:-1]) != int(number[-1]):
        raise InvalidChecksum()
    return True


def is_valid(number):
    """
    Returns True/False if the number conforms to the standard ISO6346. Unlike
    the validate function, this will not raise ValidationError(s).
    """
    try:
        return bool(validate(number))
    except ValidationError:
        return False
