#!/usr/bin/env python3
# coding: utf-8

# update/at_postleitzahl.py - download list of Austrian postal codes
#
# Copyright (C) 2018-2019 Arthur de Jong
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

import os
import os.path

import lxml.html
import requests
import xlrd


try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


# The page that contains a link to the downloadable spreadsheet with current
# Austrian postal codes
base_url = 'https://www.post.at/en/business_advertise_products_and_services_addresses_postcodes.php'

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


def find_download_url():
    """Extract the spreadsheet URL from the Austrian Post website."""
    response = requests.get(base_url)
    response.raise_for_status()
    document = lxml.html.document_fromstring(response.content)
    url = [
        a.get('href')
        for a in document.findall('.//a[@href]')
        if '/downloads/PLZ_Verzeichnis' in a.get('href')][0]
    return urljoin(base_url, url.split('?')[0])


def get_postal_codes(download_url):
    """Download the Austrian postal codes spreadsheet."""
    response = requests.get(download_url)
    response.raise_for_status()
    workbook = xlrd.open_workbook(
        file_contents=response.content, logfile=open(os.devnull, 'w'))
    sheet = workbook.sheet_by_index(0)
    rows = sheet.get_rows()
    # the first row contains the column names
    columns = [column.value.lower() for column in next(rows)]
    # the other rows contain data
    for row in rows:
        data = dict(zip(
            columns,
            [column.value for column in row]))
        if data['adressierbar'].lower() == 'ja':
            yield (
                data['plz'],
                data['ort'],
                regions.get(data['bundesland']))


if __name__ == '__main__':
    # download/parse the information
    download_url = find_download_url()
    # print header
    print('# generated from %s downloaded from' %
          os.path.basename(download_url))
    print('# %s' % base_url)
    # build an ordered list of postal codes
    for code, location, region in sorted(get_postal_codes(download_url)):
        print('%s location="%s" region="%s"' % (code, location, region))
