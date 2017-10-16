# ncf.py - functions for handling Dominican Republic invoice numbers
# coding: utf-8
#
# Copyright (C) 2017 Arthur de Jong
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

# Development of this functionality was funded by iterativo | http://iterativo.do

"""NCF (Números de Comprobante Fiscal, Dominican Republic receipt number).

The NCF is used to number invoices and other documents for the purposes of
tax filing. The number is 19 digits long and consists of a letter (A or P) to
indicate that the number was assigned by the taxpayer or the DGIT, followed a
2-digit business unit number, a 3-digit location number, a 3-digit mechanism
identifier, a 2-digit document type and a 8-digit serial number.

More information:

 * https://www.dgii.gov.do/et/nivelContribuyentes/Presentaciones%20contribuyentes/Número%20de%20Comprobantes%20Fiscales%20(NCF).pdf

>>> validate('A020010210100000005')
'A020010210100000005'
>>> validate('Z020010210100000005')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' ').strip().upper()


# The following document types are known:
#  01 invoices for fiscal declaration (or tax reporting)
#  02 invoices for final consumer
#  03 debit note
#  04 credit note (refunds)
#  11 informal supplier invoices (purchases)
#  12 single income record
#  13 minor expenses invoices (purchases)
#  14 invoices for special customers (tourists, free zones)
#  15 invoices for the government

def validate(number):
    """Check if the number provided is a valid NCF."""
    number = compact(number)
    if len(number) != 19:
        raise InvalidLength()
    if number[0] not in 'AP' or not number[1:].isdigit():
        raise InvalidFormat()
    if number[9:11] not in (
            '01', '02', '03', '04', '11', '12', '13', '14', '15'):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number provided is a valid NCF."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
