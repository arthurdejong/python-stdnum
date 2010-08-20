# imei.py - functions for handling International Mobile Equipment Identity
#           (IMEI) numbers
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

"""Module for handling IMEI (International Mobile Equipment Identity)
numbers, used to identify mobile phones.

>>> is_valid('35686800-004141-20')
True
>>> is_valid('35-417803-685978-1') # incorrect check digit
False
>>> compact('35686800-004141-20')
'3568680000414120'
>>> format('354178036859789')
'35-417803-685978-9'
>>> format('35686800-004141', add_check_digit=True)
'35-686800-004141-8'
>>> imei_type('35686800-004141-20')
'IMEISV'
"""


def compact(number):
    """Convert the IMEI number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = number.replace(' ','').replace('-','').strip().upper()
    return number

def imei_type(number):
    """Check the passed number and returns 'IMEI', 'IMEISV' or None (for
    invalid) for checking the type of number passed."""
    try:
        number = compact(number)
    except:
        return None
    if len(number) == 14: # IMEI without check digit
        return 'IMEI' if number.isdigit() else None
    if len(number) == 15: # IMEI with check digit
        from stdnum import luhn
        return 'IMEI' if luhn.is_valid(number) else None
    elif len(number) == 16:
        return 'IMEISV' if number.isdigit() else None
    else:
        return None

def is_valid(number):
    """Checks to see if the number provided is a valid IMEI (or IMEISV)
    number."""
    return imei_type(number) is not None

def format(number, separator='-', add_check_digit=False):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    if len(number) == 14 and add_check_digit:
        from stdnum import luhn
        number += luhn.calc_check_digit(number)
    number = ( number[:2], number[2:8], number[8:14], number[14:] )
    return separator.join(x for x in number if x)
