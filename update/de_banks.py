#!/usr/bin/env python3
# coding: utf-8

# update/de_banks.py - script to download the Bankleitzahl file from the
#                      Deutsche Bundesbank
#
# Copyright (C) 2026 Claude-Alain Martin
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
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

"""This script downloads the list of German bank codes (Bankleitzahlen) with
the institution, BIC and place as published by the Deutsche Bundesbank."""

import csv
import io
import os.path
import re

import requests


# The download page lists the current edition of the file; the file's own
# URL changes with every edition, so it is found on the page.
download_page = (
    'https://www.bundesbank.de/de/aufgaben/unbarer-zahlungsverkehr/'
    'serviceangebot/bankleitzahlen/download-bankleitzahlen-602592')

# The file that is looked up on the download page (semicolon-separated CSV).
download_file = 'blz-aktuell-csv-data.csv'


# The user agent that will be passed in requests
user_agent = 'Mozilla/5.0 (compatible; python-stdnum updater; +https://arthurdejong.org/python-stdnum/)'


def find_download_url(html):
    """Return the URL of the CSV file from the download page."""
    match = re.search(r'href="([^"]*%s)"' % re.escape(download_file), html)
    if not match:
        raise ValueError('%s not found on %s' % (download_file, download_page))
    url = match.group(1)
    if url.startswith('/'):
        url = 'https://www.bundesbank.de' + url
    return url


def get_values(csv_reader):
    """Return values (blz, bic, bank, city, deleted, successor) from the CSV.

    The file has one row per institution and bank code (Merkmal 1) and extra
    rows for branches that use the code of another institution (Merkmal 2);
    only the former describe the code itself."""
    # skip first row (header)
    try:
        next(csv_reader)
    except StopIteration:
        pass  # ignore empty CSV
    for row in csv_reader:
        if len(row) < 13 or row[1] != '1':
            continue
        blz, _merkmal, bank, _plz, city, _short, _pan, bic = row[:8]
        deleted = row[11] == '1'
        successor = row[12] if row[12] not in ('', '00000000') else ''
        yield blz, bic, bank.strip(), city.strip(), deleted, successor


if __name__ == '__main__':
    response = requests.get(download_page, timeout=30, headers={'User-Agent': user_agent})
    response.raise_for_status()
    download_url = find_download_url(response.text)
    response = requests.get(download_url, timeout=30, headers={'User-Agent': user_agent})
    response.raise_for_status()
    csv_reader = csv.reader(io.StringIO(response.content.decode('latin-1')), delimiter=';')
    print('# generated from %s downloaded from' % os.path.basename(download_url))
    print('# %s' % download_page)
    for blz, bic, bank, city, deleted, successor in get_values(csv_reader):
        info = '%s' % blz
        if bic:
            info += ' bic="%s"' % bic
        if bank:
            info += ' bank="%s"' % bank
        if city:
            info += ' city="%s"' % city
        if deleted:
            info += ' deleted="True"'
        if successor:
            info += ' successor="%s"' % successor
        print(info)
