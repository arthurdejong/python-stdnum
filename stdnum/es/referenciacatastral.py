# referenciacatastral.py - functions for handling Spanish real state ids
# coding: utf-8
#
# Copyright (C) 2016 David García Garzón
# Copyright (C) 2016 Arthur de Jong
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

"""Referencia Catastral (Spanish real estate property id)

The cadastral reference code is an id for real estates in Spain
issued by Dirección General del Catastro (General Directorate of Land
Registry) of the Ministerio de Hacienda (Tresury Ministry) of Spain.
It has 20 digits, being numbers and capital letters including spanish Ñ.
First 14 digits identify the parcel, next 4 are a sequence number
identifying different properties within the parcel,
and the last 2 are two checksum letters.

The parcel is identified diferently in urban, non-urban or
special (infrastructure) states:

* Urban states
    * 7 digits: (numeric) block sequence within cartographic sheet,
        and parcel sequence within the block.
    * 7 digits: (alphanum) cartographic sheet where the block centroid is.

* Non-urban states:
    * 2 digits: (numeric) Province or more exactly, ministerial delegation
    * 3 digits: (numeric) Municipality
    * 1 digits: (letter) Sector
    * 3 digits: (numeric) Polygon
    * 5 digits: (numeric) Parcel

* Special states:
    * BICE code: (2 digits, a number and a letter)
        * Energy infrastructure
            * 1E: Thermal power plant
            * 1G: Regasification terminal
            * 1R: Oil refinery
            * 1N: Nuclear power plant
            * 1H: Hydro power plant
        * Hydro
            * 2P: Dam
        * Roads and highways
            * 3A: Tolled highway
            * 3C: Tolled road
            * 3T: Tolled tunnel
        * Ports and airports
            * 4A: Airports
            * 4P: Comercial ports
    * Province (major if many) (2 digits)
    * Municipality (3 digits)
    * Scope (1 letter, leter)
        * E: National
        * A: Autonomous Comunity
        * P: Province
        * M: Municipality
    * Number of municipalities it extends (2 digits, numbers)
    * Abreviated denomination (4 digits, letters)


The control digit check algorithm is based on Javascript
implementation by Vicente Sancho that can be found at
http://trellat.es/validar-la-referencia-catastral-en-javascript/

More information:

* http://www.catastro.meh.es/esp/referencia_catastral_1.asp (Spanish)
* http://www.catastro.meh.es/documentos/05042010_P.pdf (Spanish)

>>> compact('7837301-VG8173B-0001 TT')
'7837301VG8173B0001TT'

>>> format('7837301VG8173B0001TT') # Urban: Lanteira town hall
'7837301 VG8173B 0001 TT'
>>> format('4A08169P03PRAT0001LR') # Special: BCN Airport
'4A08169 P03PRAT 0001 LR'

>>> validate('7837301 VG8173B 0001 TT') # Valid
'7837301VG8173B0001TT'
>>> validate('783301 VG8173B 0001 TT') # Missing digit
Traceback (most recent call last):
    ...
InvalidLength: Wrong length for cadastral reference \
'783301VG8173B0001TT', should be 20
>>> validate('7837301/VG8173B 0001 TT') # non alphanum
Traceback (most recent call last):
    ...
InvalidFormat: Found invalid digits '/'
>>> validate('7837301 VG8173B 0001 NN') # bad control digits
Traceback (most recent call last):
    ...
InvalidChecksum: Control code should be TT instead of NN

>>> is_valid('7837301VG8173B0001TT')
True
>>> is_valid('7837301VG8173B0001NN')
False

"""

from stdnum.exceptions import *
from stdnum.util import clean


_valids = u'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789'


def compact(number):
    return clean(number, ' -').strip().upper()


def format(number):
    number = compact(number)
    return ' '.join([
        number[0:7],
        number[7:14],
        number[14:18],
        number[18:20]
        ])


def validate(number):
    number = compact(number)
    invalidchars = ''.join(c for c in number if c not in _valids)
    if invalidchars:
        raise InvalidFormat(
            "Found invalid digits '{}'".format(invalidchars))

    # TODO: rustic ones are 19?
    if len(number) != 20:
        raise InvalidLength(
            "Wrong length for cadastral reference '{}', "
            "should be 20".format(number))

    def controlCode(string):
        posweight = [13, 15, 12, 5, 4, 17, 9, 21, 3, 7, 1]
        dcletter = 'MQWERTYUIOPASDFGHJKLBZX'
        dc = 0
        for i, c in enumerate(string):
            try:
                charvalue = int(c)
            except ValueError:
                charvalue = _valids.index(c)+1
            dc += posweight[i]*charvalue
        dc %= 23
        return dcletter[dc]

    dc1 = controlCode(number[0:7] + number[14:18])
    dc2 = controlCode(number[7:14] + number[14:18])

    if dc1+dc2 != number[18:]:
        raise InvalidChecksum(
            "Control code should be {} instead of {}"
            .format(dc1+dc2, number[18:]))

    return number


def is_valid(number):
    """Checks to see if the number provided is a valid Cadastral Reference."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
