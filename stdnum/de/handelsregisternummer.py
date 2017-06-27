# handelsregisternummer.py - functions for handling German company registry id
# coding: utf-8
#
# Copyright (C) 2015 Holvi Payment Services Oy
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

""" Handelsregisternummer (German company register number).

The number consists of the court where the company has registered, the type
of register and the individual number

The type of the register is either HRA or HRB where the letter "B" stands
for HR section B, where limited liability companies and corporations are
entered (GmbH's and AG's). There is also a section HRA for business
partnerships (OHG's, KG's etc.). In other words: businesses in section
HRB are limited liability companies, while businesses in HRA have personally
liable partners.

>>> validate('Aachen HRA 11223')
u'Aachen HRA 11223'

>>> validate('Frankfurt/Oder GnR 11223')
u'Frankfurt/Oder GnR 11223'

>>> validate('Bad Homburg v.d.H. PR 11223')
u'Bad Homburg v.d.H. PR 11223'

>>> validate('Ludwigshafen a.Rhein (Ludwigshafen) VR 11223')
u'Ludwigshafen a.Rhein (Ludwigshafen) VR 11223'

>>> validate('Berlin (Charlottenburg) HRA 11223 B')
u'Berlin (Charlottenburg) HRA 11223 B'

>>> validate('Berlin (Charlottenburg) HRB 11223B')
u'Berlin (Charlottenburg) HRB 11223 B'

>>> validate('Berlin (Charlottenburg) HRA 11223 B', return_parts=True)
(u'Berlin (Charlottenburg)', 'HRA', '11223 B')

>>> validate('Berlin (Charlottenburg) HRB 11223B', return_parts=True)
(u'Berlin (Charlottenburg)', 'HRB', '11223 B')

>>> validate('Berlin (Charlottenburg) HRA 11223BB')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.

>>> validate('Berlin (Charlottenburg) HRA 11223 BB')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.

>>> validate('0 HRB 44123')
u'Aachen HRB 44123'

>>> validate('160 HRB 44123')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.

>>> validate('Aachen HRC 44123')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.

"""

import re
from stdnum.exceptions import *
from stdnum.util import clean

GERMAN_COURTS = [
    u"Aachen",
    u"Altenburg",
    u"Amberg",
    u"Ansbach",
    u"Apolda",
    u"Arnsberg",
    u"Arnstadt",
    u"Aschaffenburg",
    u"Augsburg",
    u"Aurich",
    u"Bad Hersfeld",
    u"Bad Homburg v.d.H.",
    u"Bad Kreuznach",
    u"Bad Langensalza",
    u"Bad Lobenstein",
    u"Bad Oeynhausen",
    u"Bad Salzungen",
    u"Bamberg",
    u"Bayreuth",
    u"Berlin (Charlottenburg)",
    u"Bielefeld",
    u"Bochum",
    u"Bonn",
    u"Braunschweig",
    u"Bremen",
    u"Bückeburg",
    u"Chemnitz",
    u"Coburg",
    u"Coesfeld",
    u"Cottbus",
    u"Darmstadt",
    u"Deggendorf",
    u"Delmenhorst",
    u"Dortmund",
    u"Dresden",
    u"Duisburg",
    u"Düren",
    u"Düsseldorf",
    u"Eisenach",
    u"Erfurt",
    u"Eschwege",
    u"Essen",
    u"Flensburg",
    u"Frankfurt am Main",
    u"Frankfurt/Oder",
    u"Freiburg",
    u"Friedberg",
    u"Fritzlar",
    u"Fulda",
    u"Fürth",
    u"Gelsenkirchen",
    u"Gera",
    u"Gießen",
    u"Gotha",
    u"Göttingen",
    u"Greiz",
    u"Gütersloh",
    u"Hagen",
    u"Hamburg",
    u"Hamm",
    u"Hanau",
    u"Hannover",
    u"Heilbad Heiligenstadt",
    u"Hildburghausen",
    u"Hildesheim",
    u"Hof",
    u"Homburg",
    u"Ilmenau",
    u"Ingolstadt",
    u"Iserlohn",
    u"Jena",
    u"Kaiserslautern",
    u"Kassel",
    u"Kempten (Allgäu)",
    u"Kiel",
    u"Kleve",
    u"Koblenz",
    u"Köln",
    u"Königstein",
    u"Korbach",
    u"Krefeld",
    u"Landau",
    u"Landshut",
    u"Langenfeld",
    u"Lebach",
    u"Leipzig",
    u"Lemgo",
    u"Limburg",
    u"Lübeck",
    u"Ludwigshafen a.Rhein (Ludwigshafen)",
    u"Lüneburg",
    u"Mainz",
    u"Mannheim",
    u"Marburg",
    u"Meiningen",
    u"Memmingen",
    u"Merzig",
    u"Mönchengladbach",
    u"Montabaur",
    u"Mühlhausen",
    u"München",
    u"Münster",
    u"Neubrandenburg",
    u"Neunkirchen",
    u"Neuruppin",
    u"Neuss",
    u"Nienburg (Weser)",
    u"Nordhausen",
    u"Nürnberg",
    u"Offenbach am Main",
    u"Oldenburg (Oldenburg)",
    u"Osnabrück",
    u"Osterholz-Scharmbeck",
    u"Ottweiler",
    u"Paderborn",
    u"Passau",
    u"Pinneberg",
    u"Pößneck",
    u"Potsdam",
    u"Recklinghausen",
    u"Regensburg",
    u"Rinteln",
    u"Rostock",
    u"Rotenburg (Wümme) (Rotenburg/Wümme)",
    u"Rudolstadt",
    u"Saalfeld",
    u"Saarbrücken",
    u"Saarlouis",
    u"Schweinfurt",
    u"Schwerin",
    u"Siegburg",
    u"Siegen",
    u"Sömmerda",
    u"Sondershausen",
    u"Sonneberg",
    u"Stadthagen",
    u"Stadtroda",
    u"Steinfurt",
    u"Stendal",
    u"St. Ingbert (St Ingbert)",
    u"Stralsund",
    u"Straubing",
    u"Stuttgart",
    u"St. Wendel (St Wendel)",
    u"Suhl",
    u"Tostedt",
    u"Traunstein",
    u"Ulm",
    u"Vechta",
    u"Verden (Aller)",
    u"Völklingen",
    u"Walsrode",
    u"Weiden i. d. OPf.",
    u"Weimar",
    u"Wetzlar",
    u"Wiesbaden",
    u"Wittlich",
    u"Wuppertal",
    u"Würzburg",
    u"Zweibrücken"
]

REGISTRY_TYPES = [
    'HRA',
    'HRB',
    'PR',
    'GnR',
    'VR',
]


def validate(number, return_parts=False):
    """
    Validate the format of a German company registry number.

    Parse number backwards. Expect the last part to be the number,
    the next to be the registry, and the rest to be the court.

    Returns a string with the parts, but optionally return a tuple
    with them.
    """

    # Return empty if something unsplittable was sent in
    try:
        parts = number.split()
    except AttributeError:
        return ''

    if not parts:
        raise InvalidFormat()

    # At least Berlin can have a B after the digit part
    if parts[-1].isalpha():
        qualifier = parts.pop(-1)
        if len(qualifier) != 1:
            raise InvalidFormat()
    else:
        qualifier = None

    if not parts:
        raise InvalidFormat()

    number = parts.pop(-1)
    if not parts:
        raise InvalidFormat()

    # The case where there was no space between the digit and the character
    if number[-1].isalpha() and qualifier is None:
        number, qualifier = number[:-1], number[-1]

    number = clean(number, ' -./,')
    if not number.isdigit():
        raise InvalidFormat()
    elif qualifier is not None:
        number = "%s %s" % (number, qualifier)

    registry = parts.pop(-1)
    if not parts:
        raise InvalidFormat()

    if registry not in REGISTRY_TYPES:
        raise InvalidFormat(registry)

    court = ' '.join(parts)
    court = clean(court, ':').strip()
    if court.lower() not in (name.lower() for name in GERMAN_COURTS):
        try:
            ordinal = int(court)
            if ordinal < len(GERMAN_COURTS) and ordinal >= 0:
                court = GERMAN_COURTS[ordinal]
            else:
                raise InvalidFormat()
        except ValueError:
            raise InvalidFormat()
    else:
        index = [name.lower() for name in GERMAN_COURTS].index(court.lower())
        court = GERMAN_COURTS[index]

    if return_parts:
        return (court, registry, number)
    else:
        return "%s %s %s" % (court, registry, number)


def is_valid(number):
    """Checks to see if the number provided is a valid company registry number.
    This checks that the court exists and the format is correct."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
