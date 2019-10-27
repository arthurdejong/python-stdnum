#!/usr/bin/env python3

# update/cn_loc.py - script to fetch data from the CN Open Data community
#
# Copyright (C) 2014-2015 Jiangge Zhang
# Copyright (C) 2015-2019 Arthur de Jong
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

"""This script downloads birth place codes from the CN Open Data community on
Github."""

from __future__ import print_function, unicode_literals

import sys
from collections import OrderedDict
from datetime import datetime

import requests


data_url = 'https://github.com/cn/GB2260'
data_revisions = [
    'GB2260-2002',
    'GB2260-2003',
    'GB2260-200306',
    'GB2260-2004',
    'GB2260-200403',
    'GB2260-200409',
    'GB2260-2005',
    'GB2260-200506',
    'GB2260-2006',
    'GB2260-2007',
    'GB2260-2008',
    'GB2260-2009',
    'GB2260-2010',
    'GB2260-2011',
    'GB2260-2012',
    'GB2260-2013',
    'GB2260-2014',
]


def fetch_data():
    """Return the data from tab-separated revisions as one code/name dict."""
    data_collection = OrderedDict()
    for revision in data_revisions:
        response = requests.get('%s/raw/release/%s.txt' % (data_url, revision))
        response.raise_for_status()
        if response.ok:
            print('%s is fetched' % revision, file=sys.stderr)
        else:
            print('%s is missing' % revision, file=sys.stderr)
            continue
        for line in response.text.strip().split('\n'):
            code, name = line.split('\t')
            data_collection[code.strip()] = name.strip()
    return data_collection


def group_data(data_collection):
    """Filter the data and return codes with names."""
    for code, name in sorted(data_collection.items()):
        if code.endswith('00'):
            continue  # county only
        province_code = code[:2] + '0000'
        prefecture_code = code[:4] + '00'
        province_name = data_collection[province_code]
        prefecture_name = data_collection[prefecture_code]
        yield code, name, prefecture_name, province_name


if __name__ == '__main__':
    """Output a data file in the right format."""
    print("# generated from National Bureau of Statistics of the People's")
    print('# Republic of China, downloaded from %s' % data_url)
    print('# %s' % datetime.utcnow())
    data_collection = fetch_data()
    for data in group_data(data_collection):
        print('%s county="%s" prefecture="%s" province="%s"' % data)
