# rrn.py - functions for handling South Korean RRN numbers
# coding: utf-8
#
# Copyright (C) 2018 Dimitri Papadopoulos
# Copyright (C) 2016-2017 Arthur de Jong
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

"""RRN (South Korean resident registration number).

The RRN (Resident Registration Number, 주민등록번호) is used to identify
residents in the Republic of Korea. Foreigners residing in the Republic
of Korea receive an alien registration number (ARN) rather than a RRN,
which follows a different encoding pattern.

The number consists of 13 digits: YYMMDD-SBBCCNV

The first six digits code the date of birth. Note that the year is coded
with two digits.

The seventh digit S codes both the sex and the century of birth:
* 1 – male Korean citizens (born 1900–1999)
* 2 – female Korean citizens (born 1900–1999)
* 3 – male Korean citizens (2000–present)
* 4 – female Korean citizens (2000–present)
* 5 – male foreign residents in Korea (born 1900–1999)
* 6 – female foreign residents in Korea (born 1900–1999)
* 7 – male foreign residents in Korea (2000–present)
* 8 – female foreign residents in Korea (2000–present)
* 9 – male Korean citizens (born 1800–1899)
* 0 – female Korean citizens (born 1800–1899)

The four next digits BBCC code the place of birth for Koreans - or the
issuing agency for foreigners. The last two digits CC code the community
center number, which the South Korean Ministry of Public Administration
and Security keeps private. The meaning of the first two digits BB is
public:
* Seoul: 00–08
* Busan: 09–12
* Incheon: 13–15
* Gyeonggi: 16–25
* Gangwon: 26–34
* Chungcheongbuk: 35–39
* Daejeon: 40
* Chungcheongnam: 41–47
* Sejong: 44, 96
* Jeonbuk: 48–54
* Jeollanam: 55–64
* Gwangju: 65–66
* Daegu: 67–70
* Gyeongsangbuk: 71–80
* Gyeongsangnam: 81–90
* Ulsan: 85
* Jeju: 91–95

Digit N is a sequential number that differentiates those of the same sex
born on the same day in the same location.

The last digit is a check digit.

More information:
* http://www.law.go.kr/lsSc.do?tabMenuId=tab18&p1=&subMenu=1&nwYn=1&section=&tabNo=&query=%EA%B0%9C%EC%9D%B8%EC%A0%95%EB%B3%B4%20%EB%B3%B4%ED%98%B8%EB%B2%95
* https://en.wikipedia.org/wiki/Resident_registration_number
* https://techscience.org/a/2015092901/
"""

from stdnum.exceptions import *
from stdnum.util import clean
from datetime import date


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip().upper()


def calc_check_digits(number):
    """Calculate the check digit. The number passed should not have the
    check digit included."""
    checksum = 0
    multiplier = 2
    for n in number:
        checksum += multiplier * int(n)
        multiplier += 1
        if multiplier > 9:
            multiplier = 2
    return str((11 - (checksum % 11)) % 10)


def validate(number, future=True):
    """Check if the number provided is valid. This checks the length,
    formatting and check digit."""
    number = compact(number)
    if not number.isdigit():
        raise InvalidFormat()
    if len(number) != 13:
        raise InvalidLength()

    year = int(number[1:3])
    month = int(number[3:5])
    day = int(number[5:7])
    century = int(number[7])
    if century in {1, 2, 5, 6}:  # born 1900-1999
        year += 1900
    elif century in {3, 4, 7, 8}:  # born 2000-2099
        year += 2000
    else:  # born 1800-1899
        year += 1800
    try:
        date_of_birth = date(year, month, day)
    except ValurError:
        raise InvalidComponent()
    else:
        # should we discard dates of birth in the future?
        if not future and date_of_birth > date.today():
            raise InvalidComponent()

    place_of_birth = int(number[8:10])
    if place_of_birth > 96:
        raise InvalidComponent()

    community_centre = int(number[10:12])  # TODO: find a way to check?

    if calc_check_digits(number[:-1]) != number[-1]:
        raise InvalidChecksum()

    return number


def is_valid(number):
    """Check if the number provided is valid."""
    try:
        validate(number)
    except ValidationError:
        return False
    else:
        return True


def format(number, separator=' '):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return separator.join((
        number[:1], number[1:3], number[3:5], number[5:7], number[7:10],
        number[10:13], number[13:]))
