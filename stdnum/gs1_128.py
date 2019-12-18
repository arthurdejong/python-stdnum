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

from stdnum.exceptions import *
from stdnum.util import clean


APPLICATION_CODES = {
    '00': (str, 18, False),
    '01': (str, 14, False),
    '02': (str, 14, False),
    '10': (str, 20, True),
    '11': (date, 6, False),
    '12': (date, 6, False),
    '13': (date, 6, False),
    '15': (date, 6, False),
    '17': (date, 6, False),
    '20': (str, 2, False),
    '21': (str, 20, True),
    '22': (str, 29, True),
    '231': (str, 19, True),
    '232': (str, 19, True),
    '233': (str, 19, True),
    '234': (str, 19, True),
    '235': (str, 19, True),
    '236': (str, 19, True),
    '237': (str, 19, True),
    '238': (str, 19, True),
    '239': (str, 19, True),
    '230': (str, 19, True),
    '240': (str, 30, True),
    '241': (str, 30, True),
    '242': (str, 30, True),
    '243': (str, 30, True),
    '250': (str, 30, True),
    '251': (str, 30, True),
    '253': (str, 17, True),
    '254': (str, 20, True),
    '255': (str, 25, True),
    '30': (int, 8, True),
    '310': (float, 8, False),
    '311': (float, 8, False),
    '312': (float, 8, False),
    '313': (float, 8, False),
    '314': (float, 8, False),
    '315': (float, 8, False),
    '316': (float, 8, False),
    '320': (float, 8, False),
    '321': (float, 8, False),
    '322': (float, 8, False),
    '323': (float, 8, False),
    '324': (float, 8, False),
    '325': (float, 8, False),
    '326': (float, 8, False),
    '327': (float, 8, False),
    '328': (float, 8, False),
    '329': (float, 8, False),
    '330': (float, 8, False),
    '331': (float, 8, False),
    '332': (float, 8, False),
    '333': (float, 8, False),
    '334': (float, 8, False),
    '335': (float, 8, False),
    '336': (float, 8, False),
    '340': (float, 8, False),
    '341': (float, 8, False),
    '342': (float, 8, False),
    '343': (float, 8, False),
    '344': (float, 8, False),
    '345': (float, 8, False),
    '346': (float, 8, False),
    '347': (float, 8, False),
    '348': (float, 8, False),
    '349': (float, 8, False),
    '350': (float, 8, False),
    '351': (float, 8, False),
    '352': (float, 8, False),
    '353': (float, 8, False),
    '354': (float, 8, False),
    '355': (float, 8, False),
    '356': (float, 8, False),
    '357': (float, 8, False),
    '360': (float, 8, False),
    '361': (float, 8, False),
    '362': (float, 8, False),
    '363': (float, 8, False),
    '364': (float, 8, False),
    '365': (float, 8, False),
    '366': (float, 8, False),
    '367': (float, 8, False),
    '368': (float, 8, False),
    '369': (float, 8, False),
    '37': (int, 8, True),
    '390': (float, 15, True),
    '391': (str, 18, True),
    '392': (float, 15, True),
    '393': (str, 18, True),
    '400': (str, 30, True),
    '401': (str, 30, True),
    '402': (str, 17, False),
    '403': (str, 30, True),
    '410': (str, 13, False),
    '411': (str, 13, False),
    '412': (str, 13, False),
    '413': (str, 13, False),
    '414': (str, 13, False),
    '420': (str, 20, True),
    '421': (str, 15, True),
    '422': (str, 3, False),
    '423': (str, 15, True),
    '424': (str, 3, False),
    '425': (str, 3, False),
    '426': (str, 3, False),
    '7001': (str, 13, False),
    '7002': (str, 30, True),
    '7003': (str, 10, False),
    '7004': (str, 4, True),
    '7030': (str, 30, True),
    '7031': (str, 30, True),
    '7032': (str, 30, True),
    '7033': (str, 30, True),
    '7034': (str, 30, True),
    '7035': (str, 30, True),
    '7036': (str, 30, True),
    '7037': (str, 30, True),
    '7038': (str, 30, True),
    '7039': (str, 30, True),
    '8001': (str, 14, False),
    '8002': (str, 20, True),
    '8003': (str, 30, True),
    '8004': (str, 30, True),
    '8005': (float, 6, False),
    '8006': (str, 18, False),
    '8007': (str, 30, True),
    '8008': (date, 8, True),
    '8018': (str, 18, False),
    '8020': (str, 25, True),
    '8100': (str, 6, True),
    '8101': (str, 10, True),
    '8102': (str, 2, True),
    '8110': (str, 30, True),
    '8200': (str, 70, True),
    '90': (str, 30, True),
    '91': (str, 90, True),
    '92': (str, 90, True),
    '93': (str, 90, True),
    '94': (str, 90, True),
    '95': (str, 90, True),
    '96': (str, 90, True),
    '97': (str, 90, True),
    '98': (str, 90, True),
    '99': (str, 90, True),
}


def _convert_str(val):
    return str(val).strip()


def _convert_date(val):
    return datetime.strptime(val, '%y%m%d').date()


def _convert_int(val):
    return int(val)


def _convert_float(val):
    digits = float(_convert_int(val[:2]))
    value = float(_convert_int(val[2:]))
    return value / 10 ** digits


CONVERTERS = {
    str: _convert_str,
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


def info(code, stopchar=None):
    """
    Return a dictionary containing the gs1-128 info embeded in code

    Each application code's data is converted to the proper python:
        * str: for string values
        * datetime.date: for date values
        * int: for int values
        * float: for numeric values
    Escape characters are also removed

    If stopchar is set it will be used as FNC1 to determine the end
    of a variable application code
    """
    code = compact(code)
    queue = deque(code)

    data = {}
    identifier = ''
    while queue:
        identifier += queue.popleft()
        if identifier not in APPLICATION_CODES:
            if len(identifier) < 4:
                continue
            raise InvalidComponent(identifier)
        converter, length, variable = APPLICATION_CODES[identifier]
        value = ''
        for _ in range(length):
            try:
                char = queue.popleft()
                # If it's a stop char do not continue
                if variable and stopchar and char == stopchar:
                    break
                value += char
            except IndexError:
                pass
        data[identifier] = CONVERTERS[converter](value)
        identifier = ''
    return data


def encode(data, stopchar=None):
    """
    Return a GS1-128 code for application identifiers contained in the data
    dictionary

    Use the compacted version of the code

    If stopchar is set it will be used as FNC1 representation and variable
    fields will not include blank fields
    """
    code = ''
    # Use sorted to keep a logical order of keys
    for key in sorted(data.keys()):
        if key in APPLICATION_CODES:
            encoder, length, variable = APPLICATION_CODES[key]
            code += key
            value = ENCODERS[encoder](data[key], length)
            # Add stop character to make code shorter
            if variable and stopchar and len(value.rstrip()) < length:
                value = value.rstrip() + stopchar
            code += value
    # Last stopchar is not necessary
    if code and stopchar and code[-1] == stopchar:
        code = code[:-1]
    return compact(code)
