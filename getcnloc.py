#!/usr/bin/env python

# getcnloc.py - script to fetch data from the China (PRC) government site
#
# Copyright (C) 2014 Jiangge Zhang
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

from __future__ import print_function, unicode_literals

import sys
import codecs
from urlparse import urljoin
from operator import itemgetter
from datetime import datetime

import requests
import lxml.html


revisions_url = 'http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/'


def make_etree(response, encoding='utf-8'):
    if not response.ok:
        args = (response.status_code, response.reason, response.url)
        print('%d %s: %s' % args, file=sys.stderr)
        sys.exit(-1)
    response.encoding = encoding
    return lxml.html.fromstring(response.text)


def iter_revisions():
    html = make_etree(requests.get(revisions_url))
    anchors = html.xpath('.//div[@class="center_list"]/ul/li/a')
    for anchor in anchors:
        url = urljoin(revisions_url, anchor.attrib['href'])
        date_text = anchor.findtext('.//span/*[@class="cont_tit02"]')
        date = datetime.strptime(date_text, '%Y-%m-%d').date()
        yield url, date


def iter_records(url):
    html = make_etree(requests.get(url))
    lines = html.xpath('.//div[@class="xilan_con"]//p/text()')
    for line in lines:
        try:
            city_code, city_name = line.strip().split()
        except ValueError:
            if line.strip():
                print('invalid line: %r' % line, file=sys.stderr)
        else:
            yield city_code.strip(), city_name.strip()


def group_records():
    url, _ = max(iter_revisions(), key=itemgetter(1))  # latest revision

    provinces = {}
    prefectures = {}

    for city_code, city_name in iter_records(url):
        province_code = city_code[:2]
        prefecture_code = city_code[2:4]
        county_code = city_code[4:6]

        county_name = None

        if prefecture_code == '00':
            provinces[province_code] = city_name
        elif county_code == '00':
            prefectures[prefecture_code] = city_name
        else:
            county_name = city_name

        yield city_code, dict(
            province=provinces.get(province_code),
            prefecture=prefectures.get(prefecture_code),
            county=county_name)


def print_data_file(file):
    print("# generated from National Bureau of Statistics of the People's",
          file=file)
    print('# Republic of China, downloaded from %s' % revisions_url, file=file)
    for city_code, city_data in group_records():
        if not all(city_data.values()):
            continue
        city_pairs = ' '.join(
            '%s="%s"' % (k, v) for k, v in sorted(city_data.items()) if v)
        print('%s %s' % (city_code, city_pairs), file=file)


if __name__ == '__main__':
    if sys.stdout.isatty():
        print_data_file(sys.stdout)
    else:
        print_data_file(codecs.getwriter('utf-8')(sys.stdout))
