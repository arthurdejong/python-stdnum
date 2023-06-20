# coding=utf-8
# bis.py - functions for handling Belgian BIS numbers
#
# Copyright (C) 2023 Jeff Horemans
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

"""BIS (Belgian BIS number).


The BIS number (BIS-nummer, Numéro BIS) is a unique identification number
for individuals who are not registered in the National Register, but who
still have a relationship with the Belgian government.
This includes frontier workers, persons who own property in Belgium,
persons with Belgian social security rights but who do not reside in Belgium, etc.

The number is issued by the Belgian Crossroads Bank for Social Security (Banque
Carrefour de la sécurité sociale, Kruispuntbank voor Sociale Zekerheid) and is
constructed much in the same way as the Belgian National Number, i.e. consisting of
11 digits, encoding the person's date of birth and gender, a checksum, etc.
Other than with the national number though, the month of birth of the BIS number
is increased by 20 or 40, depending on whether the sex of the person was known
at the time or not.


More information:

* https://sma-help.bosa.belgium.be/en/faq/where-can-i-find-my-bis-number#7326
* https://www.socialsecurity.be/site_nl/employer/applics/belgianidpro/index.htm
* https://nl.wikipedia.org/wiki/Rijksregisternummer
* https://fr.wikipedia.org/wiki/Numéro_de_registre_national

>>> compact('98.47.28-997.65')
'98472899765'
>>> validate('98 47 28 997 65')
'98472899765'
>>> validate('01 49 07 001 85')
'01490700185'
>>> validate('12345678901')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('98472899765')
'98.47.28-997.65'
>>> get_birth_date('98.47.28-997.65')
datetime.date(1998, 7, 28)
>>> get_birth_year('98.47.28-997.65')
1998
>>> get_birth_month('98.47.28-997.65')
7
>>> get_gender('98.47.28-997.65')
'M'
"""

import datetime

from stdnum.be import nn
from stdnum.exceptions import *
from stdnum.util import isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the number
    of any valid separators and removes surrounding whitespace."""
    return nn.compact(number)


def _get_birth_date_parts(number):
    century = nn._checksum(number)
    # The month is incremented with 20 or 40 for BIS numbers,
    # so subtract to validate the embedded birth date in the same
    # manner as national number.
    month = int(number[2:4])
    if 20 <= month <= 32:
        month -= 20
    elif 40 <= month <= 52:
        month -= 40
    else:
        raise InvalidComponent('month must be in 20..32 or 40..52 range')

    # Create the fictitious national number version of the BIS number,
    # with recalculated checksum, based on the decreased month.
    # This way, we can reuse the nn module's functionality of extracting
    # the parts of the embedded birth date, which may be unknown.
    number = number[:2] + str(month).zfill(2) + number[4:]
    if century == 1900:
        checksum = 97 - int(number[:-2]) % 97
    else:
        checksum = 97 - int('2' + number[:-2]) % 97
    number = number[:9] + str(checksum).zfill(2)
    return nn._get_birth_date_parts(number)


def validate(number):
    """Check if the number is a valid BIS Number."""
    number = compact(number)
    if not isdigits(number) or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    _get_birth_date_parts(number)
    return number


def is_valid(number):
    """Check if the number is a valid BIS Number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    return nn.format(number)


def get_birth_year(number):
    """Return the year of the birth date."""
    year, month, day = _get_birth_date_parts(compact(number))
    return year


def get_birth_month(number):
    """Return the month of the birth date."""
    year, month, day = _get_birth_date_parts(compact(number))
    return month


def get_birth_date(number):
    """Return the date of birth."""
    year, month, day = _get_birth_date_parts(compact(number))
    if None not in (year, month, day):
        return datetime.date(year, month, day)


def get_gender(number):
    """Get the person's gender ('M' or 'F'), which for BIS
    numbers is only known if the month was incremented with 40."""
    number = compact(number)
    if int(number[2:4]) >= 40:
        return nn.get_gender(number)
