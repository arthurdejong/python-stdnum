# ncf.py - functions for handling Dominican Republic invoice numbers
# coding: utf-8
#
# Copyright (C) 2017-2018 Arthur de Jong
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

"""NCF (Números de Comprobante Fiscal, Dominican Republic receipt number).

The NCF is used to number invoices and other documents for the purpose of tax
filing. The e-CF (Comprobante Fiscal Electrónico) is used together with a
digital certificate for the same purpose. The number is either 19, 11 or 13
(e-CF) digits long.

The 19 digit number starts with a letter (A or P) to indicate that the number
was assigned by the taxpayer or the DGII, followed a 2-digit business unit
number, a 3-digit location number, a 3-digit mechanism identifier, a 2-digit
document type and a 8-digit serial number.

The 11 digit number always starts with a B followed a 2-digit document type
and a 7-digit serial number.

The 13 digit e-CF starts with an E followed a 2-digit document type and an
8-digit serial number.

More information:

 * https://www.dgii.gov.do/
 * https://dgii.gov.do/workshopProveedoresTI-eCE/Documents/Norma05-19.pdf
 * https://dgii.gov.do/cicloContribuyente/facturacion/comprobantesFiscales/Paginas/tiposComprobantes.aspx

>>> validate('E310000000005')  # format since 2019-04-08
'E310000000005'
>>> validate('B0100000005')  # format since 2018-05-01
'B0100000005'
>>> validate('A020010210100000005')  # format before 2018-05-01
'A020010210100000005'
>>> validate('Z0100000005')
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from stdnum.exceptions import *
from stdnum.util import clean, isdigits

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    return clean(number, ' ').strip().upper()


# The following document types are known:
_ncf_document_types = (
    '01',  # invoices for fiscal declaration (or tax reporting)
    '02',  # invoices for final consumer
    '03',  # debit note
    '04',  # credit note (refunds)
    '11',  # informal supplier invoices (purchases)
    '12',  # single income invoices
    '13',  # minor expenses invoices (purchases)
    '14',  # invoices for special customers (tourists, free zones)
    '15',  # invoices for the government
    '16',  # invoices for export
    '17',  # invoices for payments abroad
)

_ecf_document_types = (
    '31',  # invoices for fiscal declaration (or tax reporting)
    '32',  # invoices for final consumer
    '33',  # debit note
    '34',  # credit note (refunds)
    '41',  # supplier invoices (purchases)
    '43',  # minor expenses invoices (purchases)
    '44',  # invoices for special customers (tourists, free zones)
    '45',  # invoices for the government
    '46',  # invoices for exports
    '47',  # invoices for foreign payments
)


def validate(number):
    """Check if the number provided is a valid NCF."""
    number = compact(number)
    if len(number) == 13:
        if number[0] != 'E' or not isdigits(number[1:]):
            raise InvalidFormat()
        if number[1:3] not in _ecf_document_types:
            raise InvalidComponent()
    elif len(number) == 11:
        if number[0] != 'B' or not isdigits(number[1:]):
            raise InvalidFormat()
        if number[1:3] not in _ncf_document_types:
            raise InvalidComponent()
    elif len(number) == 19:
        if number[0] not in 'AP' or not isdigits(number[1:]):
            raise InvalidFormat()
        if number[9:11] not in _ncf_document_types:
            raise InvalidComponent()
    else:
        raise InvalidLength()
    return number


def is_valid(number):
    """Check if the number provided is a valid NCF."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def _convert_result(result):  # pragma: no cover
    """Translate SOAP result entries into dictionaries."""
    translation = {
        'NOMBRE': 'name',
        'COMPROBANTE': 'proof',
        'ES_VALIDO': 'is_valid',
        'MENSAJE_VALIDACION': 'validation_message',
        'RNC': 'rnc',
        'NCF': 'ncf',
        u'RNC / Cédula': 'rnc',
        u'RNC/Cédula': 'rnc',
        u'Nombre / Razón Social': 'name',
        u'Nombre/Razón Social': 'name',
        'Estado': 'status',
        'Tipo de comprobante': 'type',
        u'Válido hasta': 'valid_until',
        u'Código de Seguridad': 'security_code',
        'Rnc Emisor': 'issuing_rnc',
        'Rnc Comprador': 'buyer_rnc',
        'Monto Total': 'total',
        'Total de ITBIS': 'total_itbis',
        'Fecha Emisi&oacuten': 'issuing_date',
        u'Fecha Emisión': 'issuing_date',
        u'Fecha de Firma': 'signature_date',
        'e-NCF': 'ncf',
    }
    return dict(
        (translation.get(key, key), value)
        for key, value in result.items())


def _get_form_parameters(document):
    """Extracts necessary form parameters from the HTML document."""
    return {
        '__EVENTVALIDATION': document.find('.//input[@name="__EVENTVALIDATION"]').get('value'),
        '__VIEWSTATE': document.find('.//input[@name="__VIEWSTATE"]').get('value'),
       '__VIEWSTATEGENERATOR': document.find('.//input[@name="__VIEWSTATEGENERATOR"]').get('value'),
    }


def _parse_result(document, ncf):
    """Parses the HTML document to extract the result."""
    result_path = './/div[@id="cphMain_PResultadoFE"]' if ncf.startswith(
        'E') else './/div[@id="cphMain_pResultado"]'
    result = document.find(result_path)

    if result is not None:
        lbl_path = './/*[@id="cphMain_lblEstadoFe"]' if ncf.startswith(
            'E') else './/*[@id="cphMain_lblInformacion"]'
        data = {
            'validation_message': document.findtext(lbl_path).strip(),
        }
        data.update({
            key.text.strip(): value.text.strip()
            for key, value in zip(result.findall('.//th'), result.findall('.//td/span'))
            if key.text and value.text
        })
        return _convert_result(data)

    return None


def _build_post_data(rnc, ncf, form_params, buyer_rnc=None, security_code=None):
    """Builds the data dictionary for the POST request."""
    data = {
        **form_params,
        '__ASYNCPOST': "true",
        'ctl00$smMain': 'ctl00$upMainMaster|ctl00$cphMain$btnConsultar',
        'ctl00$cphMain$btnConsultar': 'Buscar',
        'ctl00$cphMain$txtNCF': ncf,
        'ctl00$cphMain$txtRNC': rnc,
    }

    if ncf.startswith('E'):
        data['ctl00$cphMain$txtRncComprador'] = buyer_rnc
        data['ctl00$cphMain$txtCodigoSeg'] = security_code

    return data

def check_dgii(rnc, ncf, buyer_rnc=None, security_code=None, timeout=30):  # pragma: no cover
    """Validate the RNC, NCF combination on using the DGII online web service.

    This uses the validation service run by the the Dirección General de
    Impuestos Internos, the Dominican Republic tax department to check
    whether the combination of RNC and NCF is valid. The timeout is in
    seconds.

    Returns a dict with the following structure for a NCF::

        {
            'name': 'The registered name',
            'status': 'VIGENTE',
            'type': 'FACTURAS DE CREDITO FISCAL',
            'rnc': '123456789',
            'ncf': 'A020010210100000005',
            'validation_message': 'El NCF digitado es válido.',
        }

    For an ECNF::

        {
            'status': 'Aceptado',
            'issuing_rnc': '1234567890123',
            'buyer_rnc': '123456789',
            'ncf': 'E300000000000',
            'security_code': '1+2kP3',
            'issuing_date': '2020-03-25',
            'signature_date': '2020-03-22',
            'total': '2203.50',
            'total_itbis': '305.10',
            'validation_message': 'Aceptado',
        }

    Will return None if the number is invalid or unknown."""
    import lxml.html
    import requests
    from stdnum.do.rnc import compact as rnc_compact  # noqa: I003
    rnc = rnc_compact(rnc)
    ncf = compact(ncf)
    if buyer_rnc:
        buyer_rnc = rnc_compact(buyer_rnc)
    url = 'https://dgii.gov.do/app/WebApps/ConsultasWeb2/ConsultasWeb/consultas/ncf.aspx'
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (python-stdnum)',
    })

    # Config retries
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[500, 502, 503, 504],
        raise_on_status=False
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))

    response = session.get(url, timeout=timeout, verify=False)
    response.raise_for_status()
    document = lxml.html.fromstring(response.text)

    # Extract necessary form parameters
    form_params = _get_form_parameters(document)

    # Build data for the POST request
    post_data = _build_post_data(
        rnc, ncf, form_params, buyer_rnc, security_code)

    response = session.post(url, data=post_data, timeout=timeout, verify=False)
    response.raise_for_status()
    document = lxml.html.fromstring(response.text)

    # Parse and return the result
    return _parse_result(document, ncf)