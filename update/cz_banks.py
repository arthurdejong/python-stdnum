#!/usr/bin/env python3
# coding: utf-8

# update/cz_banks.py - script to download Bank list from Czech National Bank
#
# Copyright (C) 2022 Petr Přikryl
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

"""This script downloads the list of banks with bank codes as used in the
IBAN and BIC codes as published by the Czech National Bank."""

import csv
import os.path
from io import StringIO

import requests


# The location of the CSV version of the bank identification codes. Also see
# https://www.cnb.cz/cs/platebni-styk/ucty-kody-bank/
download_url = 'https://www.cnb.cz/cs/platebni-styk/.galleries/ucty_kody_bank/download/kody_bank_CR.csv'


def get_values(csv_reader):
    """Return values (bank_number, bic, bank_name, certis) from the CSV."""
    # skip first row (header)
    try:
        next(csv_reader)
    except StopIteration:
        pass  # ignore empty CSV

    for row in csv_reader:
        yield row[0], row[2], row[1], row[3] == 'A'


if __name__ == '__main__':
    response = requests.get(download_url, timeout=30)
    response.raise_for_status()
    csv_reader = csv.reader(StringIO(response.content.decode('utf-8')), delimiter=';')
    print('# generated from %s downloaded from' % os.path.basename(download_url))
    print('# %s' % download_url)
    for bank_number, bic, bank, certis in get_values(csv_reader):
        info = '%s' % bank_number
        if bic:
            info += ' bic="%s"' % bic
        if bank:
            info += ' bank="%s"' % bank
        if certis:
            info += ' certis="%s"' % certis
        print(info)
