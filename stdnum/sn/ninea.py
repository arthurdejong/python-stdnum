# ninea.py - functions for handling Senegal NINEA numbers
# coding: utf-8
#
# Copyright (C) 2023 Leandro Regueiro
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

"""NINEA (Numéro d'Identification national des Entreprises et Associations,
Senegal tax number).

This number consists of 7 digits (in practive it is sometimes 9 digits, the
first two being zeroes). It is usually followed by a Tax Identification Code
called COFI.

The COFI consists of 3 alphanumeric characters. The first one is a digit:

* 0: taxpayer subject to the real scheme, not subject to VAT.
* 1: taxpayer subject to the single global contribution (TOU).
* 2: taxpayer subject to the real scheme and subject to VAT.

The second character is a letter that indicates the tax center of attachment:

* A: Dakar Plateau 1.
* B: Dakar Plateau 2.
* C: Grand Dakar.
* D: Pikine.
* E: Rufisque.
* F: Thiès.
* G: Big Business Center.
* H: Luga.
* J: Diourbel.
* K: Saint-Louis.
* L: Tambacounda.
* M: Kaolack.
* N: Fatick.
* P: A.
* Q: Kolda.
* R: remediated Parcels.
* S: Liberal Professions.
* T: Guédiawaye.
* U: Dakar-Medina.
* V: Dakar Freedom.
* W: Matam.
* Z: Medium Business Centre.

The third character is a digit that indicates the legal form of the taxpayer:

* 1: Individual-Natural person.
* 2: SARL.
* 3: SA.
* 4: Simple Limited Partnership.
* 5: Share Sponsorship Company.
* 6: GIE.
* 7: Civil Society.
* 8: Partnership.
* 9: Cooperative Association.
* 0: Other.

More information:

* https://www.nkac-audit.com/en/comment-lire-un-numero-d-identifiant-fiscal-unique-ninea-au-senegal/
* https://audifiscsn.com/en/2021/12/11/savoir-bien-lire-le-ninea-peut-vous-eviter-des-redressements-fiscaux/
* https://www.creationdentreprise.sn/rechercher-une-societe

>>> validate('3067221')
'3067221'
>>> validate('30672212G2')
'30672212G2'
>>> validate('306 7221')
'3067221'
>>> validate('3067221 2G2')
'30672212G2'
>>> validate('12345')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('VV34567')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('VV345670A0')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('12345679A0')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('12345670I0')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> validate('12345670AZ')
Traceback (most recent call last):
    ...
InvalidComponent: ...
>>> format('30672212G2')
'3067221 2G2'
"""  # noqa: E501

from stdnum.exceptions import *
from stdnum.util import clean, isdigits


TAX_CENTERS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N',
               'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Z')


def compact(number):
    """Convert the number to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, ' -/,').upper().strip()


def validate(number):
    """Check if the number is a valid Senegal NINEA number.

    This checks the length and formatting.
    """
    number = compact(number)
    if len(number) not in (7, 9, 10, 12):
        raise InvalidLength()
    if len(number) in (7, 9) and not isdigits(number):
        raise InvalidFormat()
    if len(number) in (10, 12) and not isdigits(number[:-3]):
        raise InvalidFormat()
    if len(number) in (10, 12) and number[-3] not in ('0', '1', '2'):
        raise InvalidComponent()
    if len(number) in (10, 12) and number[-2] not in TAX_CENTERS:
        raise InvalidComponent()
    if len(number) in (10, 12) and not isdigits(number[-1]):
        raise InvalidComponent()
    return number


def is_valid(number):
    """Check if the number is a valid Senegal NINEA number."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    if len(number) in (7, 9):
        return number
    return ' '.join([number[:-3], number[-3:]])
