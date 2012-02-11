# util.py - common utility functions
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

"""Common functions for other stdnum modules."""


def clean(number, deletechars):
    """Remove the specified characters from the supplied number.

    >>> clean('123-456:78 9', ' -:')
    '123456789'
    """
    return ''.join(x for x in number if x not in deletechars)


def digitsum(numbers):
    """Returns the sum of the individual digits of the provided numbers.

    >>> digitsum([12, 55])
    13
    """
    # note: this only works for two-digit numbers
    return sum((x // 10) + (x % 10) for x in numbers)
