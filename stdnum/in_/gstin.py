# gstin.py - functions for handling Indian GST identification number
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

"""GSTIN (Goods and Services Tax identification number, Indian VAT number).

The Goods and Services Tax identification number (GSTIN) is a 15 digt unique
identifier assigned to all tax paying entities in India registered under the
Goods and Services Tax (GST) Act, 2017.

Each GSTIN begins with a 2 digit State/Union Territory (UT) Code, as per 2011
census, in the range 01 to 35. The next 10 characters are PAN of the holder.
The 13th character is an alphanumeric digit that represents the number of
GSTIN registrations made in a state/UT for same the PAN. Max. 35 registrations
are allowed. The 14th character is "Z" by default. The last character is an
alphanumeric check digit calculated using a custom algorithm.

More information: 

* https://bajajfinserv.in/insights/what-is-goods-and-service-tax-identification-number
* https://en.wikipedia.org/wiki/Goods_and_Services_Tax_(India)

>>> validate('27AAPFU0939F1ZV')
'27AAPFU0939F1ZV'
>>> validate('27AAPFU0939F1Z')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('369296450896540')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('36AAPFU0939F1ZV')    # invalid state code
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('27AAPXU0939F1ZV')    # invalid PAN
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('27AAPFU0939F1ZO')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> info('27AAPFU0939F1ZV')['state_or_ut']
'Maharashtra'
"""

import re
import stdnum.exceptions as e

from stdnum.in_ import gstin_ca
from stdnum.in_ import pan
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""

    return clean(number, " -").upper().strip()


def validate(number):
    """Check if the number provided is a valid GSTIN. This checks the length,
    formatting, embedded PAN and check digit."""

    GSTIN_RE = re.compile(r"^[0-3][0-9][A-Z]{5}[0-9]{4}[A-Z][1-9A-Z][Z][0-9A-Z]$")
    number = compact(number)
    if len(number) != 15:
        raise e.InvalidLength()
    if not GSTIN_RE.match(number):
        raise e.InvalidFormat()
    if not 1 <= int(number[:2]) <= 35:
        raise e.InvalidComponent()
    pan.validate(number[2:12])
    gstin_ca.validate(number)
    return number


def is_valid(number):
    """Check if the number provided is a valid GSTIN. This checks the length,
    formatting, embedded PAN and check digit."""

    try:
        return bool(validate(number))
    except e.ValidationError:
        return False


def info(number):
    """Provide information that can be decoded locally from GSTIN (without
    API).

    More information can be viewed on the GST website. Search by:

    * GSTIN: https://services.gst.gov.in/services/searchtp
    * PAN: https://services.gst.gov.in/services/searchtpbypan
    """

    STATE_UT_CODES = {
        "01": "Jammu and Kashmir",
        "02": "Himachal Pradesh",
        "03": "Punjab",
        "04": "Chandigarh",
        "05": "Uttarakhand",
        "06": "Haryana",
        "07": "Delhi",
        "08": "Rajasthan",
        "09": "Uttar Pradesh",
        "10": "Bihar",
        "11": "Sikkim",
        "12": "Arunachal Pradesh",
        "13": "Nagaland",
        "14": "Manipur",
        "15": "Mizoram",
        "16": "Tripura",
        "17": "Meghalaya",
        "18": "Assam",
        "19": "West Bengal",
        "20": "Jharkhand",
        "21": "Orissa",
        "22": "Chattisgarh",
        "23": "Madhya Pradesh",
        "24": "Gujarat",
        "25": "Daman and Diu",
        "26": "Dadar and Nagar Haveli",
        "27": "Maharashtra",
        "28": "Andhra Pradesh",
        "29": "Karnataka",
        "30": "Goa",
        "31": "Lakshadweep",
        "32": "Kerala",
        "33": "Tamil Nadu",
        "34": "Puducherry",
        "35": "Anadaman and Nicobar Islands",
    }
    number = compact(number)
    pan_info = pan.info(number[2:12])
    state_ut = STATE_UT_CODES.get(number[:2])
    reg_count = gstin_ca.to_int(number[12])
    return {
        "state_or_ut": state_ut,
        "pan_type": pan_info["card_holder_type"],
        "initial": pan_info["initial"],
        "registration_count": reg_count,
    }
