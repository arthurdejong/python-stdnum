#!/usr/bin/env python3
# coding: utf-8

# update/nz_banks.py - script to download Bank list from Bank Branch Register
#
# Copyright (C) 2019-2024 Arthur de Jong
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
New Zealand bank account numbers."""

import io
import re
from collections import OrderedDict, defaultdict

import openpyxl
import requests


# The page that contains a link to the latest XLS version of the codes.
download_url = 'https://www.paymentsnz.co.nz/resources/industry-registers/bank-branch-register/download/xlsx/'


def get_values(sheet):
    """Return rows from the worksheet as a dict per row."""
    rows = sheet.iter_rows()
    # the first row has column names
    columns = [column.value.lower().replace(' ', '_') for column in next(rows)]
    # go over rows with values
    for row in rows:
        yield dict(zip(columns, [column.value for column in row]))


def branch_list(branches):
    """Return a compact representation of a list of branch numbers."""
    branches = sorted(int(b) for b in branches)
    first = None
    prev = None
    res = ''
    for branch in branches:
        if first is not None and branch == prev + 1:
            # this branch is consecutive to the previous: make a range
            if prev > first:
                res = res[:-5]
            res += '-%04d' % branch
            prev = branch
        else:
            # this is a new branch, add a new one to the list
            res += ',%04d' % branch
            first = prev = branch
    return res.lstrip(',')


if __name__ == '__main__':
    # parse the download as an XLS
    response = requests.get(download_url, timeout=30)
    response.raise_for_status()
    content_disposition = response.headers.get('content-disposition', '')
    filename = re.findall(r'filename=?(.+)"?', content_disposition)[0].strip('"')
    workbook = openpyxl.load_workbook(io.BytesIO(response.content), read_only=True)
    sheet = workbook.worksheets[0]
    # print header
    print('# generated from %s downloaded from' % filename)
    print('# %s' % download_url)
    # build banks list from spreadsheet
    banks = defaultdict(dict)
    for line in get_values(sheet):
        banks[line['bank_number']]['bank'] = line['bank_name']
        branches = banks[line['bank_number']].setdefault('branches', OrderedDict())
        branches.setdefault((line['branch_information'], line['bic']), list()).append(line['branch_number'])
    # output bank information
    for bank_number in sorted(banks.keys()):
        bank = banks[bank_number]
        print('%s bank="%s"' % (bank_number, bank['bank']))
        for (branch, bic), branch_numbers in bank['branches'].items():
            print(' %s%s branch="%s"' % (
                branch_list(branch_numbers), ' bic="%s"' % bic if bic else '', branch))
