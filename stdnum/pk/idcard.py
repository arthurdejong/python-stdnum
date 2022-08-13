
# idcard.py - functions for handling Computrized National Identity Card (CNIC) 
# and Smart National Identity Card (SNIC) of Pakistani citizen
# Author: Quantum Novice (Syed Haseeb Shah)
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

"""CNIC/SNIC (Pakistani Computerized National Identity Card)

NADRA is a government organization that issues an identifier to 
Pakistani citizens.


More Information:
* https://en.wikipedia.org/wiki/CNIC_(Pakistan)
* https://www.geo.tv/latest/157233-secret-behind-every-digit-of-the-cnic-number


>>> validate('34201-0891231-8')
'3420108912318'
>>> validate('42201-0397640-8')
'4220103976408'
>>> format('3420108912318')
'34201-0891231-8'
"""

from enum import IntEnum, unique
from stdnum.exceptions import *
from stdnum.util import clean, isdigits


# Valid Province IDs
PROVINCES = {
            1:  'KP',
            2:  'FATA',
            3:  'Punjab',
            4:  'Sindh', 
            5:  'Balochistan',
            6:  'Islamabad',
            7:  'Gilgit-Baltistan',
            }
@unique
class Province(IntEnum):
    KP                  = 1
    FATA                = 2
    PUNJAB              = 3
    SINDH               = 4
    BALOCHISTAN         = 5
    ISLAMABAD           = 6
    GILGIT_BALTISTAN    = 7

    @classmethod
    def keys(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def assign(cls, value):
        for item in list(cls):
            if item.value == int(value):
                return Province[item.name]
        raise InvalidChecksum

@unique
class Gender(IntEnum):
    """
    Enum for gender
    """
    MALE = 0
    FEMALE = 1

def compact(number:str) -> str:
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, '-').strip()


def get_description(number):
    """
    Get detailed description of the CNIC.
    It also serves as a checksum. The return
    obect is for information and possible future
    use case. 
    """
    
    # The first five digit is locality
    locality        = number[0:5]

    family_id       = number[5:12]
    gender          = number[-1]

    province        = number[0]
    division        = number[1]
    district        = number[2]
    tehsil          = number[3]
    union_council   = number[4]

    if province in Province.keys():
         raise InvalidComponent()
    else:
        province = Province.assign(province)

    if int(gender) in [1, 3, 5, 7, 9]:
        gender = Gender.MALE
    elif int(gender) in [2, 4, 6, 8]:
        gender = Gender.FEMALE
        
    return {
            'locality'  : locality,
            'family-id' : family_id,
            'gender'    : gender,
            'province'  : province,
            'division'  : division,
            'district'  : district,
            'tehsil'    : tehsil,
        'union-council' : union_council
    }
 

def calc_check_digit(number):
    """Calculate the checksum."""
    return len(number)==13

def validate(number):
    """Check if the number is a valid CNIC/SNIC. This checks the length, formatting
    and check digit."""
    number = compact(number)
    
    # This function will automatically raise exception
    # related to a checksum
    get_description(number)
    if not isdigits(number):
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()
    if not calc_check_digit(number):
        raise InvalidChecksum()
    
    return number


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join((number[0:5], number[5:12], number[-1]))


if __name__ == '__main__':
    # Taken from the internet 
    example_cnic = '34201-0891231-8'
    ccnic = compact(example_cnic)
    print(validate(ccnic))
    print(format(ccnic))

    print(get_description(ccnic))