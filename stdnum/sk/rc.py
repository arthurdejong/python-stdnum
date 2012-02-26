# rc.py - functions for handling Slovak birth numbers
# coding: utf-8
#
# Copyright (C) 2012 Arthur de Jong
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

"""RČ (Rodné číslo, the Slovak birth number).

The birth number (RČ, Rodné číslo) is the Slovak national identifier. The
number can be 9 or 10 digits long. Numbers given out after January 1st
1954 should have 10 digits. The number includes the birth date of the
person and their gender.

This number is identical to the Czech counterpart.

>>> compact('710319/2745')
'7103192745'
>>> is_valid('7103192745')
True
>>> is_valid('991231123')
True
>>> is_valid('7103192746')  # invalid check digit
False
>>> is_valid('1103492745')  # invalid date
False
>>> is_valid('590312/123')  # 9 digit number in 1959
False
>>> format('7103192745')
'710319/2745'
"""

# since this number is essentially the same as the Czech counterpart
# (until 1993 the Czech Republic and Slovakia were one country)
from stdnum.cz.rc import compact, is_valid, format
__all__ = ['compact', 'is_valid', 'format']
