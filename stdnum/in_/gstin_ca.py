# gstin_ca.py - functions for performing GSTIN checksum algorithm
#
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

"""Goods and Services Tax identification number (GSTIN) Checksum Algorithm.

The GSTIN Checksum algorithm is a custom checksum algorithm designed by Goods
and Services Tax Network (GSTN) to catch errors in the identifier. 

The alphanumeric characters in the identifier are converted to int as per a
conversion table (provided below), then a series of arithmetic operations are
performed to calculate the check digit. The check digit is then converted
back to an alphanumeric character following the same table.

Conversion Table: ["0": 0 ... "9": 9, "A": 10 ... "Z": 35]

A major flaw in this algorithm is interchanging characters present at odd or
even indices does not change the check digit.

More information: 

* https://medium.com/@dhananjaygokhale/decoding-gst-number-checksum-digit-1ef2c8c53ad6

>>> checksum('27AAPFU0939F1Z')
'27AAPFU0939F1ZV'
>>> calc_check_digit('27AAPFU0939F1Z')
'V'
>>> validate('27AAPFU0939F1ZV')
'27AAPFU0939F1ZV'
>>> validate('27A@PF$0939F!ZV')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('27AAPFU0939F1ZO')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
"""

import stdnum.exceptions as e

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""

    return clean(number, " -").upper().strip()


# Not using a dict as conversion table, the code was looking very inelegant.
# Instead wrote two functions to handle the conversion.


def to_int(char: str) -> int:
    """Convert character to integer as per the conversion table. Takes an
    alphanumeric str of length = 1"""

    # Digits are returned as int. Unicode code point (UCP) [int] of uppercase
    # letters are returned after subtracting 55 from them. Why 55? UCP of "A"
    # is 65. 65 - 55 = 10. See the Conversion Table above.

    if len(char) > 1:
        raise e.InvalidLength()
    if char.isalnum() is False:
        raise e.InvalidComponent()
    if char.isalpha() is True and char.isupper() is True:
        return ord(char) - 55
    return int(char)


def to_char(index: int) -> str:
    """Convert integer to character as per the conversion table. Takes an int
    between 0 and 35, inclusive."""

    # Integers [0,9] are returned as str. 55 is added to integers [10, 35]
    # and returned after converting them to Unicode string.

    if 0 <= index <= 9:
        return str(index)
    elif 10 <= index <= 35:
        return chr(index + 55)
    raise e.InvalidComponent()


def checksum(number):
    """Calculate checksum of an alphanumeric str. Returns the str with check
    digit attached to it at the end."""

    number = compact(number)
    if number.isalnum() is True:
        c = 0
        for i in range(len(number)):
            val = to_int(number[i])
            if i % 2 == 0:
                c += (val // 36) + (val % 36)
            else:
                val *= 2
                c += (val // 36) + (val % 36)
        check_digit_int = 36 - (c % 36)
        return number + to_char(check_digit_int)
    raise e.InvalidFormat()


def calc_check_digit(number):
    """Calculate check digit of an alphanumeric str."""

    return checksum(number)[-1]


def validate(number):
    """Check if the number provided passes the checksum."""

    number = compact(number)
    if number.isalnum() is False:
        raise e.InvalidFormat()
    if checksum(number[:-1]) != number:
        raise e.InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided passes the checksum."""

    try:
        return bool(validate(number))
    except e.ValidationError:
        return False
