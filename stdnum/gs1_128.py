# gs1_128.py - functions for handling GS1-128 codes
#
# Copyright (C) 2019 Sergi Almacellas Abellana
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

"""GS1-128.

Module for handling GS1-128.

GS1-128 (also called EAN-128) is an standard for embedding data with
Application Identifiers (AI)

>>> compact('(01)38425876095074(17)181119(37)1 ')
'013842587609507417181119371'
>>> encode({'01': '38425876095074'})
'0138425876095074'
>>> info('0138425876095074')
{'01': '38425876095074'}
"""

from collections import deque
from datetime import date, datetime

from stdnum.util import clean


APPLICATION_CODES = {
    '00': (str, 18),
    '01': (str, 14),
    '02': (str, 14),
    '10': (str, 20),
    '11': (date, 6),
    '12': (date, 6),
    '13': (date, 6),
    '15': (date, 6),
    '17': (date, 6),
    '20': (str, 2),
    '21': (str, 20),
    '22': (str, 29),
    '231': (str, 19),
    '232': (str, 19),
    '233': (str, 19),
    '234': (str, 19),
    '235': (str, 19),
    '236': (str, 19),
    '237': (str, 19),
    '238': (str, 19),
    '239': (str, 19),
    '230': (str, 19),
    '240': (str, 30),
    '241': (str, 30),
    '242': (str, 30),
    '243': (str, 30),
    '250': (str, 30),
    '251': (str, 30),
    '253': (str, 17),
    '254': (str, 20),
    '255': (str, 25),
    '30': (int, 8),
    '310': (float, 8),
    '311': (float, 8),
    '312': (float, 8),
    '313': (float, 8),
    '314': (float, 8),
    '315': (float, 8),
    '316': (float, 8),
    '320': (float, 8),
    '321': (float, 8),
    '322': (float, 8),
    '323': (float, 8),
    '324': (float, 8),
    '325': (float, 8),
    '326': (float, 8),
    '327': (float, 8),
    '328': (float, 8),
    '329': (float, 8),
    '330': (float, 8),
    '331': (float, 8),
    '332': (float, 8),
    '333': (float, 8),
    '334': (float, 8),
    '335': (float, 8),
    '336': (float, 8),
    '340': (float, 8),
    '341': (float, 8),
    '342': (float, 8),
    '343': (float, 8),
    '344': (float, 8),
    '345': (float, 8),
    '346': (float, 8),
    '347': (float, 8),
    '348': (float, 8),
    '349': (float, 8),
    '350': (float, 8),
    '351': (float, 8),
    '352': (float, 8),
    '353': (float, 8),
    '354': (float, 8),
    '355': (float, 8),
    '356': (float, 8),
    '357': (float, 8),
    '360': (float, 8),
    '361': (float, 8),
    '362': (float, 8),
    '363': (float, 8),
    '364': (float, 8),
    '365': (float, 8),
    '366': (float, 8),
    '367': (float, 8),
    '368': (float, 8),
    '369': (float, 8),
    '37': (int, 8),
    '390': (float, 15),
    '391': (str, 18),
    '392': (float, 15),
    '393': (str, 18),
    '400': (str, 30),
    '401': (str, 30),
    '402': (str, 17),
    '403': (str, 30),
    '410': (str, 13),
    '411': (str, 13),
    '412': (str, 13),
    '413': (str, 13),
    '414': (str, 13),
    '420': (str, 20),
    '421': (str, 15),
    '422': (str, 3),
    '423': (str, 15),
    '424': (str, 3),
    '425': (str, 3),
    '426': (str, 3),
    '7001': (str, 13),
    '7002': (str, 30),
    '7003': (str, 10),
    '7004': (str, 4),
    '7030': (str, 30),
    '7031': (str, 30),
    '7032': (str, 30),
    '7033': (str, 30),
    '7034': (str, 30),
    '7035': (str, 30),
    '7036': (str, 30),
    '7037': (str, 30),
    '7038': (str, 30),
    '7039': (str, 30),
    '8001': (str, 14),
    '8002': (str, 20),
    '8003': (str, 30),
    '8004': (str, 30),
    '8005': (float, 6),
    '8006': (str, 18),
    '8007': (str, 30),
    '8008': (date, 8),
    '8018': (str, 18),
    '8020': (str, 25),
    '8100': (str, 6),
    '8101': (str, 10),
    '8102': (str, 2),
    '8110': (str, 30),
    '8200': (str, 70),
    '90': (str, 30),
    '91': (str, 90),
    '92': (str, 90),
    '93': (str, 90),
    '94': (str, 90),
    '95': (str, 90),
    '96': (str, 90),
    '97': (str, 90),
    '98': (str, 90),
    '99': (str, 90),
}


def _convert_date(val):
    return datetime.strptime(val, '%y%m%d').date()


def _convert_int(val):
    return int(val)


def _convert_float(val):
    digits = float(_convert_int(val[:2]))
    value = float(_convert_int(val[2:]))
    return value / 10 ** digits


CONVERTERS = {
    date: _convert_date,
    int: _convert_int,
    float: _convert_float,
}


def _encode_string(val, length):
    return val.ljust(length)


def _encode_date(val, length):
    return val.strftime('%y%m%d')


def _encode_int(val, length):
    return _encode_string(str(val), length)


def _encode_float(val, length):
    number, decimals = str(val).split('.')
    digits = str(len(decimals)).rjust(2, '0')
    number = number.rjust(6 - len(decimals), '0')
    return _encode_string(digits + number + decimals, length)


ENCODERS = {
    str: _encode_string,
    date: _encode_date,
    int: _encode_int,
    float: _encode_float,
}


def compact(number):
    """
    Convert the GS1-128 to the minimal representation.

    This strips the number of any valid separators and removes surrounding
    whitespace.
    """
    return clean(number, '()').strip()


def info(code):
    """
    Return a dictionary containing the gs1-128 info embeded in code

    Each application code's data is converted to the proper python:
        * str: for string values
        * datetime.date: for date values
        * int: for int values
        * float: for numeric values

    Escape characters are also removed
    """
    code = compact(code)
    queue = deque(code)

    data = {}
    identifier = ''
    while queue:
        identifier += queue.popleft()
        if identifier in APPLICATION_CODES:
            converter, length = APPLICATION_CODES[identifier]
            value = ''
            for _ in range(length):
                try:
                    value += queue.popleft()
                except IndexError:
                    pass
            data[identifier] = CONVERTERS.get(converter, lambda a: a)(value)
            identifier = ''
    return data


def encode(data):
    """
    Return a GS1-128 code for application identifiers contained in the data
    dictionary

    Use the compacted version of the code
    """
    code = ''
    # Use sorted to keep a logical order of keys
    for key in sorted(data.keys()):
        if key in APPLICATION_CODES:
            encoder, length = APPLICATION_CODES[key]
            code += key
            code += ENCODERS[encoder](data[key], length)
    return compact(code)
