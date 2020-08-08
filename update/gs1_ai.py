#!/usr/bin/env python3

# update/gs1_ai.py - script to get GS1 application identifiers
#
# Copyright (C) 2019 Arthur de Jong
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

"""This script downloads GS1 application identifiers from the GS1 web site."""

import datetime
import json
import re

import lxml.html
import requests


# the location of the GS1 application identifiers
download_url = 'https://www.gs1.org/standards/barcodes/application-identifiers'


def fetch_ais():
    """Download application identifiers frm the GS1 website."""
    response = requests.get(download_url)
    document = lxml.html.document_fromstring(response.content)
    element = document.findall('.//script[@type="application/ld+json"]')[1]
    for entry in json.loads(element.text)['@graph']:
        yield (
            entry['skos:prefLabel'].strip(),             # AI
            entry['gs1meta:formatAIvalue'].strip()[3:],  # format
            entry['gs1meta:requiresFNC1'],               # require FNC1
            [x['@value'] for x in entry['schema:name'] if x['@language'] == 'en'][0].strip(),
            [x['@value'] for x in entry['schema:description'] if x['@language'] == 'en'][0].strip())


def group_ai_ranges():
    """Combine downloaded application identifiers into ranges."""
    first = None
    prev = (None, ) * 5
    for value in sorted(fetch_ais()):
        if value[1:] != prev[1:]:
            if first:
                yield (first, *prev)
            first = value[0]
        prev = value
    yield (first, *prev)


if __name__ == '__main__':
    print('# generated from %s' % download_url)
    print('# on %s' % datetime.datetime.utcnow())
    for ai1, ai2, format, require_fnc1, name, description in group_ai_ranges():
        _type = 'str'
        if re.match(r'^(N8\+)?N[0-9]*[.]*[0-9]+$', format) and 'date' in description.lower():
            _type = 'date'
        elif re.match(r'^N[.]*[0-9]+$', format) and 'count' in description.lower():
            _type = 'int'
        ai = ai1
        if ai1 != ai2:
            if len(ai1) == 4:
                ai = ai1[:3]
                _type = 'decimal'
            else:
                ai = '%s-%s' % (ai1, ai2)
        print('%s format="%s" type="%s"%s name="%s" description="%s"' % (
            ai, format, _type,
            ' fnc1="1"' if require_fnc1 else '',
            name, description))
