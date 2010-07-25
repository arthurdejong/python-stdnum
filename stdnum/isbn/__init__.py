# __init__.py - functions for handling ISBNs
#
# Copyright (C) 2010 Arthur de Jong
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

"""Module for handling ISBNs (International Standard Book Number). This
module handles both numbers in ISBN10 (10-digit) and ISBN13 (13-digit)
format.

>>> validate('978-9024538270')
True
>>> validate('978-9024538271') # incorrect check digit
False
>>> compact('1-85798-218-5')
'1857982185'
>>> format('9780471117094')
'978-0-471-11709-4'
>>> format('1857982185')
'1-85798-218-5'
>>> isbn_type('1-85798-218-5')
'ISBN10'
>>> isbn_type('978-0-471-11709-4')
'ISBN13'
>>> to_isbn13('1-85798-218-5')
'978-1-85798-218-3'
"""


def compact(number):
    """Convert the ISBN to the minimal representation. This strips the number
    of any valid ISBN separators and removes surrounding whitespace."""
    number = number.replace(' ','').replace('-','').strip().upper()
    if len(number) == 9:
        number = '0' + number
    return number

def _calc_isbn10_check_digit(number):
    """Calculate the ISBN check digit for 10-digit numbers. The number passed
    should not have the check bit included."""
    check = sum( (i + 1) * int(number[i]) for i in range(len(number)) ) % 11
    return 'X' if check == 10 else str(check)

def _calc_isbn13_check_digit(number):
    """Calculate the ISBN check digit for 13-digit numbers. The number passed
    should not have the check bit included."""
    return str((10 - sum( (2 * (i % 2) + 1) * int(number[i]) for i in range(len(number)))) % 10)

def isbn_type(number):
    """Check the passed number and returns 'ISBN13', 'ISBN10' or None (for
    invalid) for checking the type of number passed."""
    number = compact(number)
    if len(number) == 10:
        if not number[:-1].isdigit():
            return None
        if _calc_isbn10_check_digit(number[:-1]) != number[-1]:
            return None
        return 'ISBN10'
    elif len(number) == 13:
        if not number.isdigit():
            return None
        if _calc_isbn13_check_digit(number[:-1]) != number[-1]:
            return None
        return 'ISBN13'
    else:
        return None

def validate(number):
    """Checks to see if the number provided is a valid ISBN (either a legacy
    10-digit one or a 13-digit one). This checks the length and the check
    bit but does not check if the group and publisher are valid (use split()
    for that)."""
    return isbn_type(number) is not None

def to_isbn13(number):
    """Convert the number to ISBN13 format."""
    number = number.strip()
    min_number = compact(number)
    if len(min_number) == 13:
        return number # nothing to do, already ISBN13
    # put new check digit in place
    number = number[:-1] + _calc_isbn13_check_digit('978' + min_number[:-1])
    # add prefix
    if ' ' in number:
        return '978 ' + number
    elif '-' in number:
        return '978-' + number
    else:
        return '978' + number

def split(number):
    """Split the specified ISBN into an EAN.UCC prefix, a group prefix, a
    registrant, an item number and a check-digit. If the number is in ISBN10
    format the returned EAN.UCC prefix is '978'."""
    import ranges
    # clean up number
    number = compact(number)
    # get Bookland prefix if any
    if len(number) == 10:
        oprefix = ''
        prefix = '978'
    else:
        oprefix = prefix = number[:3]
        number = number[3:]
    # get group
    group, number = ranges.lookup(prefix, number)
    publisher, number = ranges.lookup('%s-%s' % (prefix, group), number)
    itemnr = number[:-1]
    check = number[-1]
    return ( oprefix, group, publisher, itemnr, check )

def format(number, separator='-'):
    """Reformat the passed number to the standard format with the EAN.UCC
    prefix (if any), the group prefix, the registrant, the item number and
    the check-digit separated (if possible) by the specified separator.
    Passing an empty separator should equal compact() though this is less
    efficient."""
    return separator.join(x for x in split(number) if x)
