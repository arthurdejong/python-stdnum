# -*- coding: utf-8 -*-
# steuernummer.py - functions for handling German tax numbers
# Copyright (C) 2017 Holvi Payment Services
# Copyright (C) 2012, 2013 Arthur de Jong
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
"""steuernummer (German tax number).
https://de.wikipedia.org/wiki/Steuernummer
The number is 10 or 11 digits long for the long schema and 13 digits for the
new schema. The number might have one or two opening characters based on the
city of registeration in the new schema.
The number should have a checkup letter based on Mod 11 - 10, but in reality
a lot of actual registered numbers did not abide to the checks in tests.
>>> compact(' 181/815/0815 5')
'18181508155'
>>> validate('181/815/08155')
'181/815/08155'
>>> validate('201/123/12340', 'Sachsen')
'201/123/12340'
>>> validate('4151081508156', 'Thüringen')
'4151081508156'
>>> validate('4151181508156', 'Thüringen')
Traceback (most recent call last):
    ...
InvalidFormat: ...
>>> validate('136695978')
Traceback (most recent call last):
    ...
InvalidLength: ...
"""
from stdnum.exceptions import (
    InvalidLength,
    InvalidFormat
)
from stdnum.util import clean


def compact(number):
    """
    Convert the number to the minimal representation. This strips the
    number of any valid separators ' -./,' and removes surrounding whitespace.
    """
    number = clean(number, ' -./,').upper().strip()
    return number


state_opening_character = {
    'Baden-Württemberg': {
        'standard': '',
        'bund': '28'
    },
    'Bayern': {
        'standard': '',
        'bund': '9'
    },
    'Berlin': {
        'standard': '',
        'bund': '11'
    },
    'Brandenburg': {
        'standard': '0',
        'bund': '30'
    },
    'Bremen': {
        'standard': '',
        'bund': '24'
    },
    'Hamburg': {
        'standard': '',
        'bund': '22'
    },
    'Hessen': {
        'standard': '0',
        'bund': '26'
    },
    'Mecklenburg-Vorpommern': {
        'standard': '0',
        'bund': '40'
    },
    'Niedersachsen': {
        'standard': '',
        'bund': '23'
    },
    'Nordrhein-Westfalen': {
        'standard': '',
        'bund': '5'
    },
    'Rheinland-Pfalz': {
        'standard': '',
        'bund': '27'
    },
    'Saarland': {
        'standard': '0',
        'bund': '10'
    },
    'Sachsen': {
        'standard': '2',
        'bund': '32'
    },
    'Sachsen-Anhalt': {
        'standard': '1',
        'bund': '31'
    },
    'Schleswig-Holstein': {
        'standard': '',
        'bund': '21'
    },
    'Thüringen': {
        'standard': '1',
        'bund': '41'
    }
}


def get_state_opening_characters(state, schema):
    """
    Return a string of the expected openeing chracters of that state.
    The return value will depend on the specification for that state and the
    schema type, schema type should be:
    standard: For old standard schema (Standardschema der Länder) or
    (Standardschema)
    bund: For the new federal schema (Vereinheitlichtes Bundesschema) or
    (Bundesschema)
    Use state name as the refernce in the wikipedia article.
    """
    return state_opening_character[state][schema]


def check_number_acceptable_to_state(number, state, schema):
    """
    Check if the number is acceptable to the state by checking the opening
    charicters for the state and the schema against the opening charicters of
    the provided numbers.
    """
    opening_chars = get_state_opening_characters(state, schema)
    if number.startswith(opening_chars):
        return number
    raise InvalidFormat('This identifier is not acceptable for %s.' % state)


def validate_bund_schema(number, state):
    """Return the number if valid, raises an exception otherwise"""
    if state:
        check_number_acceptable_to_state(number, state, 'bund')
    # In Bundesschema, the fourth char is always a zero.
    if not number[4] == '0':
        raise InvalidFormat()
    return number


def validate_standard_schema(number, state):
    """Return the number if valid, raises an exception otherwise"""
    if state:
        check_number_acceptable_to_state(number, state, 'standard')
    return number


def validate(number, state=None):
    """
    Checks to see if the number provided is a valid tax number.
    This checks the length and formatting.
    """
    clean_number = compact(number)
    if not clean_number.isdigit():
        raise InvalidFormat('The number contains letter.')
    if len(clean_number) == 13:
        return validate_bund_schema(number, state)

    elif len(clean_number) in [10, 11]:
        return validate_standard_schema(number, state)

    raise InvalidLength()


def is_valid(number, state=None):
    """
    Return Bool if the identifier is valid or not.
    optional (state), if specified, the opening characters of the number will
    be tested against the state known opening characters.
    """
    try:
        return bool(validate(number=number, state=state))
    except InvalidLength:
        return False
    except InvalidFormat:
        return False
