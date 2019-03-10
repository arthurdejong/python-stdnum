#!/usr/bin/env python
# coding: utf-8

# update/nz_banks.py - script to download Bank list from Bank Branch Register
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

"""This script downloads the list of banks with bank codes as used in the
New Zealand bank account numbers."""

import os.path
import re
from collections import OrderedDict, defaultdict

import requests
import xlrd


try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


# The page that contains a link to the latest XLS version of the codes.
download_url = (
    'https://www.paymentsnz.co.nz' +
    '/resources/industry-registers/bank-branch-register/')


def find_download_url():
    """Find the spreadsheet URL on the New Zealand Bank Branch Register."""
    response = requests.get(download_url)
    soup = BeautifulSoup(response.content)
    url = soup.find(
        'a',
        attrs=dict(
            href=re.compile(r'/documents/.*/Bank_Branch_Register_.*.xls')))['href']
    return urljoin(download_url, url)


def get_values(sheet):
    """Return rows from the worksheet as a dict per row."""
    rows = sheet.get_rows()
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
    # download/parse the information
    url = find_download_url()
    # parse the download as an XLS
    response = requests.get(url)
    workbook = xlrd.open_workbook(file_contents=response.content)
    sheet = workbook.sheet_by_index(0)
    # print header
    print('# generated from %s downloaded from ' %
          os.path.basename(url))
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
