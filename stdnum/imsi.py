# imsi.py - functions for handling International Mobile Subscriber Identity
#           (IMSI) numbers
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

"""IMSI (International Mobile Subscriber Identity).

The IMSI (International Mobile Subscriber Identity) is used to identify
mobile phone users (the SIM).

>>> is_valid('429011234567890')
True
>>> is_valid('439011234567890')  # unknown MCC
False
>>> split('429011234567890')
('429', '01', '1234567890')
>>> split('310150123456789')
('310', '150', '123456789')
>>> info('460001234567890')['mcc']
'460'
>>> str(info('460001234567890')['country'])
'China'
"""

from stdnum.util import clean


def compact(number):
    """Convert the IMSI number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def split(number):
    """Split the specified IMSI into a Mobile Country Code (MCC),
    a Mobile Network Code (MNC), a Mobile Station Identification Number (MSIN)."""
    from stdnum import numdb
    # clean up number
    number = compact(number)
    # split the number
    return tuple(numdb.get('imsi').split(number))


def info(number):
    """Return a dictionary of data about the supplied number."""
    from stdnum import numdb
    # clean up number
    number = compact(number)
    # split the number
    info = dict(number=number)
    mcc_info, mnc_info, msin_info = numdb.get('imsi').info(number)
    info['mcc'] = mcc_info[0]
    info.update(mcc_info[1])
    info['mnc'] = mnc_info[0]
    info.update(mnc_info[1])
    info['msin'] = msin_info[0]
    info.update(msin_info[1])
    return info


def is_valid(number):
    """Checks to see if the number provided is a valid IMSI."""
    try:
        number = compact(number)
    except:
        return False
    return len(number) in (14, 15) and \
           number.isdigit() and \
           len(split(number)) == 3
