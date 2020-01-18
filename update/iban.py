#!/usr/bin/env python3

# update/iban.py - script to download and parse data from the IBAN registry
#
# Copyright (C) 2011-2019 Arthur de Jong
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

"""This script downloads data from SWIFT (the Society for Worldwide Interbank
Financial Telecommunication which is the official IBAN registrar) to get
the data needed to correctly parse and validate IBANs."""

import csv
from collections import defaultdict

import requests


# The place where the current version of
# swift_standards_infopaper_ibanregistry_1.txt can be downloaded.
download_url = 'https://www.swift.com/node/11971'


def get_country_codes(line):
    """Return the list of country codes this line has."""
    # simplest case first
    if len(line['IBAN prefix country code (ISO 3166)']) == 2:
        return [line['IBAN prefix country code (ISO 3166)']]
    # fall back to parsing the IBAN structure
    return [x.strip()[:2] for x in line['iban structure'].split(',')]


if __name__ == '__main__':
    response = requests.get(download_url)
    response.raise_for_status()
    print('# generated from swift_standards_infopaper_ibanregistry_1.txt,')
    print('# downloaded from %s' % download_url)
    values = defaultdict(dict)
    # the file is CSV but the data is in columns instead of rows
    for row in csv.reader(response.iter_lines(decode_unicode=True), delimiter='\t', quotechar='"'):
        # skip first row
        if row and row[0] != 'Data element':
            # first column contains label
            for i, c in enumerate(row[1:]):
                values[i][row[0]] = c
    # output the collected data
    for i, data in values.items():
        bban = data['BBAN structure']
        if not(bban) or bban.lower() == 'n/a':
            bban = data['IBAN structure']
        bban = bban.replace(' ', '')
        cc = data['IBAN prefix country code (ISO 3166)'][:2]
        cname = data['Name of country']
        if bban.startswith(cc + '2!n'):
            bban = bban[5:]
        # print country line
        print('%s country="%s" bban="%s"' % (cc, cname, bban))
        # TODO: some countries have a fixed check digit value
        # TODO: some countries have extra check digits
        # TODO: use "Bank identifier position within the BBAN" field
        #       to add labels to the ranges (Bank identifier and Branch
        #       Identifier)
