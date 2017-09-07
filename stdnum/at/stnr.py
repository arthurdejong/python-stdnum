# -*- coding: utf-8 -*-
# stnr.py - functions for handling Austrian tax number
# coding: utf-8
#
# Copyright (C) 2017 Holvi Payment Services Oy
# Copyright (C) 2017 Arthur de Jong
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
""" steuernummer (Austrian tax number)
A number issued by a tax office in Austria to tax businesses, the number is
9 numerical digits long. The first two digits represent the tax office which
issued the number. The latter 7 digits represent the tax id.
https://dienstgeber.ooegkk.at/portal27/dgooegkkportal/content/contentWindow?viewmode=content&contentid=10007.681672
The tax offices specified in a list on the tax authority website here:
https://service.bmf.gv.at/Service/Anwend/Behoerden/show_mast.asp?Typ=SM&DisTyp=FA
>>> validate('38/1234567')
'381234567'
>>> validate(number='38/1234567', office='Bruck Eisenstadt Oberwart')
'381234567'
>>> is_valid('38/1234567')
True
>>> is_valid(number='38/1234567', office='Bruck Eisenstadt Oberwart')
True
"""
from stdnum.exceptions import *
from stdnum.util import clean

tax_offices_codes = {
    'Burgenland': {
        '38': {
            'tax_office': 'Bruck Eisenstadt Oberwart',
        },
    },
    'Kärnten': {
        '57': {
            'tax_office': 'Klagenfurt',
        },
        '61': {
            'tax_office': 'Spittal Villach',
        },
        '59': {
            'tax_office': 'St. Veit Wolfsberg',
        },
    },
    'Niederösterreich': {
        '15': {
            'tax_office': 'Amstetten Melk Scheibbs',
        },
        '16': {
            'tax_office': 'Baden Mödling',
        },
        '38': {
            'tax_office': 'Bruck Eisenstadt Oberwart',
        },
        '18': {
            'tax_office': 'Gänserndorf Mistelbach',
        },
        '22': {
            'tax_office': 'Hollabrunn Korneuburg Tulln',
        },
        '29': {
            'tax_office': 'Lilienfeld St. Pölten',
        },
        '33': {
            'tax_office': 'Neunkirchen Wr. Neustad',
        },
        '23': {
            'tax_office': 'Waldviertel',
        },
    },

    'Oberösterreich': {
        '41': {
            'tax_office': 'Braunau Ried Schärding',
        },
        '52': {
            'tax_office': 'Freistadt Rohrbach Urfahr',
        },
        '53': {
            'tax_office': 'Gmunden Vöcklabruck',
        },
        '54': {
            'tax_office': 'Grieskirchen Wels',
        },
        '51': {
            'tax_office': 'Kirchdorf Perg Steyr',
        },
        '46': {
            'tax_office': 'Linz',
        },
    },
    'Salzburg': {
        '93': {
            'tax_office': 'Salzburg-Land',
        },
        '91': {
            'tax_office': 'Salzburg-Stadt',
        },
        '90': {
            'tax_office': 'St. Johann Tamsweg Zell am See',
        },
    },
    'Steiermark': {
        '65': {
            'tax_office': 'Bruck Leoben Mürzzuschlag',
        },
        '72': {
            'tax_office': 'Deutschlandsberg Leibnitz Voitsberg',
        },
        '68': {
            'tax_office': 'Graz-Stadt',
        },
        '69': {
            'tax_office': 'Graz-Umgebung',
        },
        '71': {
            'tax_office': 'Judenburg Liezen',
        },
        '67': {
            'tax_office': 'Oststeiermark',
        },
    },
    'Tirol': {
        '81': {
            'tax_office': 'Innsbruck',
        },
        '82': {
            'tax_office': 'Kitzbühel Lienz',
        },
        '83': {
            'tax_office': 'Kufstein Schwaz',
        },
        '84': {
            'tax_office': 'Landeck Reutte',
        },
    },
    'Vorarlberg': {
        '97': {
            'tax_office': 'Bregenz',
        },
        '98': {
            'tax_office': 'Feldkirch',
        },
    },
    'Wien': {
        '08': {
            'tax_office': 'Wien 12/13/14 Purkersdorf',
        },
        '09': {
            'tax_office': 'Wien 1/23',
        },
        '12': {
            'tax_office': 'Wien 2/20/21/22',
        },
        '03': {
            'tax_office': 'Wien 3/6/7/11/15 Schwechat Gerasdorf',
        },
        '04': {
            'tax_office': 'Wien 4/5/10',
        },
        '06': {
            'tax_office': 'Wien 8/16/17',
        },
        '07': {
            'tax_office': 'Wien 9/18/19 Klosterneuburg',
        },
    },

}


def get_all_codes_dict():
    """Return a dict with opening chars and their tax offices"""
    offices = {}
    for _, state_dict in tax_offices_codes.items():
        offices.update(state_dict)
    return offices


def validate_acceptable_opening_chars(number):
    """Validate whether the opening chars are acceptable in
    any tax office"""
    opening_chars = number[:2]
    if opening_chars not in get_all_codes_dict():
        raise InvalidFormat(
            'The opening characters do not belong to any tax office'
        )
    return number


def validate_opening_chars_to_office(number, office):
    """Check if the opening chars are acceptable in that office"""
    opening_chars = number[:2]
    office_from_chars = get_all_codes_dict()[opening_chars]['tax_office']
    if not office_from_chars == office:
        raise InvalidFormat(
            'The opening characters do not belong to this tax office'
        )
    return number


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace. Also
    cheks that there are no junk letters in the number.
    """
    return clean(number, ' -./,').strip()


def validate(number, office=None):
    """Checks to see if the number provided is a valid tax number. This checks
    the length and formatting."""
    clean_number = compact(number)
    if len(clean_number) != 9:
        raise InvalidLength()
    if not clean_number.isdigit():
        raise InvalidFormat('The number contains non numerical digits')
    if office:
        validate_opening_chars_to_office(clean_number, office)
    else:
        validate_acceptable_opening_chars(clean_number)
    return clean_number


def is_valid(number, office=None):
    """Checks to see if the number provided is a valid tax identification
    number. This checks the length, formatting and check digit."""
    try:
        return bool(validate(number, office))
    except ValidationError:
        return False
