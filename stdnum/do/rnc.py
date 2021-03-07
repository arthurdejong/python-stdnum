# rnc.py - functions for handling Dominican Republic tax registration
# coding: utf-8
#
# Copyright (C) 2015-2018 Arthur de Jong
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

# Development of this functionality was funded by iterativo | https://iterativo.do

"""RNC (Registro Nacional del Contribuyente, Dominican Republic tax number).

The RNC is the Dominican Republic taxpayer registration number for
institutions. The number consists of 9 digits.

>>> validate('1-01-85004-3')
'101850043'
>>> validate('1018A0043')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('101850042')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('131246796')
'1-31-24679-6'
"""

import json

from stdnum.exceptions import *
from stdnum.util import clean, get_soap_client, isdigits


# list of RNCs that do not match the checksum but are nonetheless valid
whitelist = set('''
101581601 101582245 101595422 101595785 10233317 131188691 401007374
501341601 501378067 501620371 501651319 501651823 501651845 501651926
501656006 501658167 501670785 501676936 501680158 504654542 504680029
504681442 505038691
'''.split())


dgii_wsdl = 'https://www.dgii.gov.do/wsMovilDGII/WSMovilDGII.asmx?WSDL'
"""The WSDL URL of DGII validation service."""


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' -').strip()


def calc_check_digit(number):
    """Calculate the check digit."""
    weights = (7, 9, 8, 6, 5, 4, 3, 2)
    check = sum(w * int(n) for w, n in zip(weights, number)) % 11
    return str((10 - check) % 9 + 1)


def validate(number):
    """Check if the number provided is a valid RNC."""
    number = compact(number)
    if not isdigits(number):
        raise InvalidFormat()
    if number in whitelist:
        return number
    if len(number) != 9:
        raise InvalidLength()
    if calc_check_digit(number[:-1]) != number[-1]:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Check if the number provided is a valid RNC."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the number to the standard presentation format."""
    number = compact(number)
    return '-'.join((number[:1], number[1:3], number[3:-1], number[-1]))


def _convert_result(result):  # pragma: no cover
    """Translate SOAP result entries into dicts."""
    translation = {
        u'Cédula/RNC': 'rnc',
        u'Nombre Comercial':'commercial_name',
        u'Régimen de pagos': 'type',
        u'Categoría':"category",
        u'Nombre/Razón Social': 'name',
        'Estado': 'status',
        u'Actividad Economica': 'activity', 
        u'Administracion Local': 'local_place', 

    }
    return dict(
        (translation.get(key, key), value)
        for key, value in result.items())


def check_dgii(number, timeout=30):  # pragma: no cover
    """Lookup the number using the DGII online web service.

    This uses the validation service run by the the Dirección General de
    Impuestos Internos, the Dominican Republic tax department to lookup
    registration information for the number. The timeout is in seconds.

    Returns a dict with the following structure::

        {
            'rnc': '123456789',     # The requested number
            'name': 'The registered name',
            'commercial_name': 'An additional commercial name',
            'status': '2',          # 1: inactive, 2: active
            'category': '0',        # always 0?
            'payment_regime': '2',  # 1: N/D, 2: NORMAL, 3: PST
        }

    Will return None if the number is invalid or unknown."""
    # this function isn't automatically tested because it would require
    # network access for the tests and unnecessarily load the online service
    number = compact(number)
    url = 'https://dgii.gov.do/app/WebApps/ConsultasWeb2/ConsultasWeb/consultas/rnc.aspx'
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (python-stdnum)',
    })

    document = lxml.html.fromstring(
    session.get(url, timeout=30).text)

    validation = document.find('.//input[@name="__EVENTVALIDATION"]').get('value')
    viewstate = document.find('.//input[@name="__VIEWSTATE"]').get('value')
    data = {
        '__EVENTVALIDATION': validation,
        '__VIEWSTATE': viewstate,
        'ctl00$cphMain$btnBuscarPorRNC': 'Buscar', # ctl00$cphMain$btnBuscarPorRazonSocial for search by name
        'ctl00$cphMain$txtRNCCedula': number, # ctl00$cphMain$txtRazonSocial change for searh for by name
    }
    # Do the actual request
    document = lxml.html.fromstring(
        session.post(url, data=data, timeout=30).text)

    result = document.find('.//div[@id="cphMain_divBusqueda"]')
    message = document.findtext('.//*[@id="cphMain_lblInformacion"]')

    if result is not None:
        hearder = []
        keys = []

        for x in result.findall('.//tr/td'): 
            if x.attrib:
                hearder.append(x.text.strip()) # On search by name the list td tag 'data-label' will be the hearders 
            else:
                keys.append(x.text.strip()) 

        if message:
            data = {
                'validation_message': message.strip(),
            }
        else:
            data = {
                'validation_message': 'Cédula/RNC es Válido',
            }

        data.update(zip(hearder, keys))
    return _convert_result(data)


def search_dgii(keyword, end_at=10, start_at=1, timeout=30):  # TODO # pragma: no cover
    """Search the DGII online web service using the keyword.

    This uses the validation service run by the the Dirección General de
    Impuestos Internos, the Dominican Republic tax department to search the
    registration information using the keyword.

    The number of entries returned can be tuned with the `end_at` and
    `start_at` arguments. The timeout is in seconds.

    Returns a list of dicts with the following structure::

        [
            {
                'rnc': '123456789',     # The found number
                'name': 'The registered name',
                'commercial_name': 'An additional commercial name',
                'status': '2',          # 1: inactive, 2: active
                'category': '0',        # always 0?
                'payment_regime': '2',  # 1: N/D, 2: NORMAL, 3: PST
                'result_number': '1',   # index of the result
            },
            ...
        ]

    Will return an empty list if the number is invalid or unknown."""
    
    """ The same structure for check_dgii but see the comments to work with this."""

