# cpf.py - functions for handling CPF numbers
# coding: utf-8
#
# Copyright (C) 2011, 2012 Arthur de Jong
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

"""CPF (Cadastro de Pessoas Físicas, Brazillian national identifier).

>>> is_valid('390.533.447-05')
True
>>> is_valid('231.002.999-00')
False
>>> compact('390.533.447-05')
'39053344705'
>>> format('23100299900')
'231.002.999-00'
"""

from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -.').strip()


def _calc_check_digits(number):
    """Calculate the check digits for the number."""
    d1 = sum((10 - i) * int(number[i]) for i in range(9))
    d1 = (11 - d1) % 11 % 10
    d2 = sum((11 - i) * int(number[i]) for i in range(9)) + 2 * d1
    d2 = (11 - d2) % 11 % 10
    return '%d%d' % (d1, d2)


def is_valid(number):
    """Checks to see if the number provided is a valid BSN. This checks
    the length and whether the check digit is correct."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) == 11 and \
           number.isdigit() and \
           int(number) > 0 and \
           _calc_check_digits(number) == number[-2:]


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return number[:3] + '.' + number[3:6] + '.' + number[6:-2] + '-' + number[-2:]
