# nir.py - functions for handling French NIR numbers
#
# Copyright (C) 2016 Dimitri Papadopoulos
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

"""NIR (French personal identification number).

The NIR (Numero d'Inscription au Repertoire national d'identification
des personnes physiques) is a 15 digit number used to identify persons
in France. All persons born in France are registered in the Repertoire
national d'identification des personnes physiques (RNIPP) and assigned
a NIR which consists of 15 digits where the two final digits are check
digits. The NIR is used by French social security and is popularly known
as the "social security number".

More information:

* http://www.insee.fr/en/methodes/default.asp?page=definitions/nir.htm

>>> validate('2 95 10 99 126 111 93')
'295109912611193'
>>> validate('295109912611199')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('295109912611193')
'2 95 10 99 126 111 93'
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' .').strip()


def validate(number):
    """Checks to see if the number provided is valid. This checks the length
    and check digit."""
    number = compact(number).upper()
    if not (number.isdigit() or (number[:5].isdigit() and number[7:].isdigit()
                                 and number[5:7] in {'2A', '2B'})):
        raise InvalidFormat()
    if len(number) != 15:
        raise InvalidLength()
    if int(number[:1]) not in {1, 2,
                               3, 4, 7, 8}:  # according to Wikipedia
        raise InvalidFormat()
    year = int(number[1:3])
    month = int(number[3:5])
    if month < 1 or (month > 12
                     and month != 62 and month != 63):  # unknown months
        raise InvalidFormat()
    department = number[5:7]
    if department in {'2A', '2B'}:
        # Corsica after 1976-01-01
        pass  # FIXME: check municipality code
    else:
        department = int(department)
        if (department >= 1 and department <= 95):
            # metropolitan France
            # Algeria and Morroco before 1964
            pass  # FIXME: check municipality code
        elif department == 96 and year < 65:
            # Tunisia before 1964
            pass  # FIXME: check municipality code
        elif department == 99:
            # foreign countries
            pass  # FIXME: check country code
        elif department in {97, 98}:
            # overseas territory
            department = int(number[5:8])
            STATUTORY_EXCEPTION = {
                984,  # Terres australes et antarctiques francaises
                986,  # Wallis-et-Futuna
                987,  # Polynesie francaise
                988,  # Nouvelle-Caledonie
                989,  # Ile de Clipperton
            }
            if ((department >= 971 and department <= 978) or
                    department in STATUTORY_EXCEPTION):
                pass  # FIXME: check municipality code
            else:
                raise InvalidFormat()
        else:
            raise InvalidFormat()
    if department == '2A':
        s = number[:5] + '19' + number[7:13]
    elif department == '2B':
        s = number[:5] + '18' + number[7:13]
    else:
        s = number[:13]
    if (97 - (int(s) % 97)) != int(number[13:]):
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is valid. This checks the length
    and check digits."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number, separator=' '):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return separator.join((number[:1], number[1:3], number[3:5], number[5:7],
                           number[7:10], number[10:13], number[13:]))
