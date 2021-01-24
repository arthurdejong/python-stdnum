#!/usr/bin/env python3
# coding: utf-8

# update/at_postleitzahl.py - download list of Austrian postal codes
#
# Copyright (C) 2018-2021 Arthur de Jong
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

"""This download list of postal codes from Austrian Post."""

from __future__ import print_function, unicode_literals

import requests


# The URL of postal codes on the Austrian open-data portal in CSV format.
download_url = 'https://data.rtr.at/api/v1/tables/plz.json'


# The list of regions that can be used in the document.
regions = {
    'B': 'Burgenland',
    'K': 'Kärnten',
    'N': 'Niederösterreich',
    'O': 'Oberösterreich',
    'Sa': 'Salzburg',
    'St': 'Steiermark',
    'T': 'Tirol',
    'V': 'Vorarlberg',
    'W': 'Wien',
}


if __name__ == '__main__':
    response = requests.get(download_url)
    response.raise_for_status()
    data = response.json()
    # print header
    print('# generated from %s' % download_url)
    print('# version %s published %s' % (
        data['version']['id'], data['version']['published']))
    # build an ordered list of postal codes
    results = []
    for row in data['data']:
        if row['adressierbar'] == 'Ja':
            results.append((str(row['plz']), row['ort'], regions[row['bundesland']]))
    for code, location, region in sorted(results):
        print('%s location="%s" region="%s"' % (code, location, region))
