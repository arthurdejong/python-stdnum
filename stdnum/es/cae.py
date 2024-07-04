# cae.py - functions for handling Spanish CAE number
# coding: utf-8
#
# Copyright (C) 2024 Quique Porta
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

"""CAE (Código de Actividad y Establecimiento).

The CAE number is a 13-digit number and that allows you to identify an
activity and the establishment in which it is carried out.

The sixth and seventh characters identify the managing office in which
the territorial registration is carried out.

And the eighth and ninth characters identify the activity that takes place.

This is the official BOE (Boletín Oficial del Estado) about the CAE number:
https://www.boe.es/boe/dias/2006/12/28/pdfs/A46098-46100.pdf

This is the online checker from the Spanish Tax Agency (Agencia Tributaria):
https://www2.agenciatributaria.gob.es/wlpl/inwinvoc/es.aeat.dit.adu.adce.cae.cw.AccW

This is the explanation of the CAE number in the Spanish Tax Agency:
https://sede.agenciatributaria.gob.es/Sede/impuestos-especiales-medioambientales/censo-impuestos-especiales-medioambientales/registro-impuestos-especiales-fabricacion.html?faqId=3cc75c714b11c710VgnVCM100000dc381e0aRCRD


>>> validate('ES00008V1488Q')
'ES00008V1488Q'
>>> validate('00008V1488')  # invalid check length
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> is_valid('ES00008V1488Q')
True
>>> is_valid('00008V1488')
False
>>> compact('ES00008V1488Q')
'ES00008V1488Q'
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Compact Spanish CAE Number"""
    return clean(number).upper().strip()


def validate(number):
    """Check if the number provided is a valid CAE number. This checks the
    length and formatting."""
    number = compact(number)

    if len(number) != 13:
        raise InvalidLength()

    if number[:2] != 'ES':
        raise InvalidFormat()

    if number[5:7] not in OFFICES:
        raise InvalidFormat()

    if number[7:9] not in ACTIVITY_KEYS:
        raise InvalidFormat()

    return number


def is_valid(number):
    """Check if the number provided is a valid CAE number. This checks the
    length and formatting."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


OFFICES = [
    '01',  # 'Álava'
    '02',  # 'Albacete'
    '03',  # 'Alicante'
    '04',  # 'Almería'
    '05',  # 'Ávila'
    '06',  # 'Badajoz'
    '07',  # 'Illes Balears'
    '08',  # 'Barcelona'
    '09',  # 'Burgos'
    '10',  # 'Cáceres'
    '11',  # 'Cádiz'
    '12',  # 'Castellón'
    '13',  # 'Ciudad Real'
    '14',  # 'Córdoba'
    '15',  # 'A Coruña'
    '16',  # 'Cuenca'
    '17',  # 'Girona'
    '18',  # 'Granada'
    '19',  # 'Guadalajara'
    '20',  # 'Guipúzcoa'
    '21',  # 'Huelva'
    '22',  # 'Huesca'
    '23',  # 'Jaén'
    '24',  # 'León'
    '25',  # 'Lleida'
    '26',  # 'La Rioja'
    '27',  # 'Lugo'
    '28',  # 'Madrid'
    '29',  # 'Málaga'
    '30',  # 'Murcia'
    '31',  # 'Navarra'
    '32',  # 'Ourense'
    '33',  # 'Oviedo'
    '34',  # 'Palencia'
    '35',  # 'Las Palmas'
    '36',  # 'Pontevedra'
    '37',  # 'Salamanca'
    '38',  # 'Santa Cruz de Tenerife'
    '39',  # 'Santander'
    '40',  # 'Segovia'
    '41',  # 'Sevilla'
    '42',  # 'Soria'
    '43',  # 'Tarragona'
    '44',  # 'Teruel'
    '45',  # 'Toledo'
    '46',  # 'Valencia'
    '47',  # 'Valladolid'
    '48',  # 'Bizcaia'
    '49',  # 'Zamora'
    '50',  # 'Zaragoza'
    '51',  # 'Cartagena'
    '52',  # 'Gijón'
    '53',  # 'Jerez de la Frontera'
    '54',  # 'Vigo'
    '55',  # 'Ceuta'
    '56',  # 'Melilla'
]

ACTIVITY_KEYS = [
    'A1',
    'B1',
    'B9',
    'B0',
    'BA',
    'C1',
    'DA',
    'EC',
    'F1',
    'V1',
    'A7',
    'AT',
    'B7',
    'BT',
    'C7',
    'DB',
    'E7',
    'M7',
    'OA',
    'OB',
    'OE',
    'OV',
    'V7',
    'B6',
    'A2',
    'A6',
    'A9',
    'A0',
    'AC',
    'AV',
    'AW',
    'AX',
    'H1',
    'H2',
    'H4',
    'H6',
    'H9',
    'H0',
    'HD',
    'HH',
    'H7',
    'H8',
    'HB',
    'HF',
    'HI',
    'HJ',
    'HK',
    'HL',
    'HM',
    'HN',
    'HT',
    'HU',
    'HV',
    'HX',
    'HZ',
    'OH',
    'HA',
    'HC',
    'HE',
    'HP',
    'HQ',
    'HR',
    'HS',
    'HW',
    'T1',
    'OT',
    'T7',
    'TT',
    'L1',
    'L2',
    'L0',
    'L3',
    'L7',
    'AF',
    'DF',
    'DM',
    'DP',
    'OR',
    'PF',
    'RF',
    'VD',
]
