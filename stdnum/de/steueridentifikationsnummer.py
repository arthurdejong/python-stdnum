# steueridentifikationsnummer.py - functions for handling German tax id
# coding: utf-8
#
# Copyright (C) 2015 Holvi Payment Services Oy
# Copyright (C) 2017 Arthur de Jong
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
"""steueridentifikationsnummer (steueridentifikationsnummer,
tax registeration number).
https://de.wikipedia.org/wiki/Steuerliche_Identifikationsnummer
The number is 11 digits long and uses the ISO 7064 Mod 11, 2 check digit
algorithm. The number has as well the following features:
     1.) one digit appears exactly twice or thrice.
     2.) one or two digits appear zero times.
     3.) and all other digits appear exactly once.

>>> compact('423 446 779 08')
'42344677908'
>>> validate('36574261809')
'36574261809'
>>> validate('116574261809')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('A6574261809')
Traceback (most recent call last):
    ...
InvalidFormat: ...
# Both 5 and 6 are repeated (not allowed).
>>> validate('36554266809')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('36574261890')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> is_valid('36574261890')
False
>>> is_valid('36574261809')
True
"""
from collections import Counter
from stdnum.exceptions import (
    InvalidLength,
    InvalidFormat,
    InvalidChecksum
)
from stdnum.iso7064 import mod_11_10
from stdnum.util import clean


def compact(number):
    """
    Convert the number to the minimal representation. This strips the
    number of any valid separators ' -./,' and removes surrounding whitespace.
    """
    number = clean(number, ' -./,').upper().strip()
    return number


def validate(number):
    """Checks to see if the number provided is a valid tax identifiication
    number. This checks the length, formatting and check digit."""
    # Number should be of length 11
    number = compact(str(number))
    if len(number) != 11:
        raise InvalidLength()
    number_list = list(number)

    # Contain only digits
    if not number.isdigit():
        raise InvalidFormat()

    # First digit in the number should not be zero.
    if number_list[0] == '0':
        raise InvalidFormat()
    # within the first ten digits one number has to appear exactly twice or
    # thrice.
    counter = Counter(number_list)
    repeated_nums = [i for i, v in counter.items() if v > 1]
    # Since we know there are 11 numbers, at least one has to be repeated.
    # One or two digits appear zero times.
    # All other digits appear only once.
    if len(repeated_nums) > 1:
        raise InvalidFormat()
    if mod_11_10.is_valid(number):
        return number
    raise InvalidChecksum()


def is_valid(number):
    """Checks to see if the number provided is a valid tax identification
    number. This checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except InvalidFormat():
        return False
    except InvalidLength():
        return False
