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

>>> validate('Achen HRA 11223')
u'Achen HRA 11223'

>>> validate('0 HRB 44123')
u'Achen HRB 44123'

>>> validate('Achen HRC 44123')
Traceback (most recent call last):
  ...
stdnum.exceptions.InvalidFormat: The number has an invalid format.

"""

import re
from stdnum.exceptions import *
from stdnum.util import clean

GERMAN_COURTS = [
    u"Achen",
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


def validate(number):
    """
    Validate the format of a German company registry number.

    First split the provided number with the HRA or HRB. Expect
    the first part to be the name of the court and the second
    part to be the registry number. Returns a cleaned representation
    of the number with the court, HRA/HRB and the number.
    """
    try:
        parts = re.split('HR(A|B)', number, flags=re.IGNORECASE)
    except TypeError:
        return ''

    if len(parts) != 3:
        raise InvalidFormat()
    if parts[1].upper() not in ['A', 'B']:
        raise InvalidFormat()
    court = clean(parts[0], ':').strip()
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
    registry = 'HR'+parts[1].upper()
    number = clean(parts[2], ' -./,').upper().strip()
    if not number.isdigit():
        raise InvalidFormat()
    return "%s %s %s" % (court, registry, number)


def is_valid(number):
    """Checks to see if the number provided is a valid company registry number.
    This checks that the court exists and the format is correct."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False
