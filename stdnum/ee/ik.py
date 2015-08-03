# ik.py - functions for handling Estonian Personal ID numbers (IK)
# coding: utf-8
#
# Copyright (C) 2012, 2013 Arthur de Jong, 2015 Tomas Karasek
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

""" (Isikukood, Estonian Personcal ID number).

>>> validate('36805280109')
'36805280109'
>>> validate('36805280108')  # incorrect check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> print get_birth_date('36805280109')
1968-05-28

"""

import stdnum.exceptions
from stdnum.util import clean
import datetime


def compact(number):
    return number.strip()


def get_birth_date(number):
    if number[0] in ['1','2']:
        century = 1800
    elif number[0] in ['3','4']:
        century = 1900
    elif number[0] in ['5','6']:
        century = 2000
    else:
        raise stdnum.exceptions.ValidationError("Wrong first number of IK: %s" % number)
    year = century + int(number[1:3])
    month = int(number[3:5])
    day = int(number[5:7])
    return datetime.date(year,month,day)


def get_check(number):
    checksum = int(number[9])
    for i, n in enumerate(number[:9]):
        checksum += int(n) * (i+1)
    check = checksum % 11
    if check == 10:
        checksum = 0
        for i, n in enumerate(number[:7]):
            checksum += int(n) * (i + 3)
        for i, n in enumerate(number[7:10]):
            checksum += int(n) * (i + 1)
        check = checksum % 11
        check = check % 10
    return str(check)


def validate(number):
    if len(number) != 11:
        raise stdnum.exceptions.InvalidLength()
    if not number.isdigit():
        raise stdnum.exceptions.InvalidFormat()
    get_birth_date(number)
    check = get_check(number)
    if check != number[10]:
        raise stdnum.exceptions.InvalidChecksum()
    return number
       

def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError, ValueError:
        return False

