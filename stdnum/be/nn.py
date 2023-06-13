# coding=utf-8
# nn.py - function for handling Belgian national numbers
#
# Copyright (C) 2021-2022 Cédric Krier
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

"""NN, NISS, RRN (Belgian national number).

The national registration number (Rijksregisternummer, Numéro de registre
national, Nationalregisternummer) is a unique identification number of
natural persons who are registered in Belgium.

The number consists of 11 digits and includes the person's date of birth and
gender. It encodes the date of birth in the first 6 digits in the format
YYMMDD. The following 3 digits represent a counter of people born on the same
date, seperated by sex (odd for male and even for females respectively). The
final 2 digits form a check number based on the 9 preceding digits.

Special cases include:

* Counter exhaustion:
  When the even or uneven day counter range for a specific date of birth runs
  out, (e.g. from 001 tot 997 for males), the first 2 digits will represent
  the birth year as normal, while the next 4 digits (birth month and day) are
  taken to be zeroes. The remaining 3 digits still represent a day counter
  which will then restart.
  When those ranges would run out also, the sixth digit is incremented with 1
  and the day counter will restart again.

* Incomplete date of birth
  When the exact month or day of the birth date were not known at the time of
  assignment, incomplete parts are taken to be zeroes, similarly as with
  counter exhaustion.
  Note that a month with zeroes can thus both mean the date of birth was not
  exactly known, or the person was born on a day were at least 500 persons of
  the same gender got a number assigned already.

* Unknown date of birth
  When no part of the date of birth was known, a fictitious date is used
  depending on the century (e.g. 01-00-1900 or 01-00-2000).

More information:

* https://nl.wikipedia.org/wiki/Rijksregisternummer
* https://fr.wikipedia.org/wiki/Numéro_de_registre_national
* https://www.ibz.rrn.fgov.be/fileadmin/user_upload/nl/rr/instructies/IT-lijst/IT000_Rijksregisternummer.pdf

>>> compact('85.07.30-033 28')
'85073003328'
>>> validate('85 07 30 033 28')
'85073003328'
>>> validate('17 07 30 033 84')
'17073003384'
>>> validate('12345678901')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('85073003328')
'85.07.30-033.28'
>>> get_birth_date('85.07.30-033 28')
datetime.date(1985, 7, 30)
>>> get_gender('85.07.30-033 28')
'M'
"""

import datetime

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


def compact(number):
    """Convert the number to the minimal representation. This strips the number
    of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').strip()
    return number


def _checksum(number):
    """Calculate the checksum and return the detected century."""
    numbers = [number]
    if int(number[:2]) + 2000 <= datetime.date.today().year:
        numbers.append('2' + number)
    for century, n in zip((19, 20), numbers):
        if 97 - (int(n[:-2]) % 97) == int(n[-2:]):
            return century
    return False


def validate(number):
    """Check if the number is a valid National Number."""
    number = compact(number)
    if not isdigits(number) or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 11:
        raise InvalidLength()
    if not _checksum(number):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number is a valid National Number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return (
        '.'.join(number[i:i + 2] for i in range(0, 6, 2)) +
        '-' + '.'.join([number[6:9], number[9:11]]))


def get_birth_date(number):
    """Return the date of birth."""
    number = compact(number)
    century = _checksum(number)
    if not century:
        raise InvalidChecksum()
    try:
        return datetime.datetime.strptime(
            str(century) + number[:6], '%Y%m%d').date()
    except ValueError:
        raise InvalidComponent()


def get_gender(number):
    """Get the person's gender ('M' or 'F')."""
    number = compact(number)
    if int(number[6:9]) % 2:
        return 'M'
    return 'F'
