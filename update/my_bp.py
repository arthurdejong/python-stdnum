#!/usr/bin/env python

# update/my_bp.py - script to download data from Malaysian government site
#
# Copyright (C) 2013-2019 Arthur de Jong
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

"""This script downloads the list of states and countries and their
birthplace code from the National Registration Department of Malaysia."""

import re
from collections import defaultdict

import requests


try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


# URLs that are downloaded
state_list_url = 'http://www.jpn.gov.my/informasi/kod-negeri/'
country_list_url = 'http://www.jpn.gov.my/en/informasi/kod-negara/'


# The user agent that will be passed in requests
user_agent = 'Mozilla/5.0 (compatible; python-stdnum updater; +https://arthurdejong.org/python-stdnum/)'


spaces_re = re.compile(r'\s+', re.UNICODE)


def clean(s):
    """Clean up the string removing unneeded stuff from it."""
    return spaces_re.sub(' ', s.replace(u'\u0096', '')).strip().encode('utf-8')


def parse(f):
    """Parse the specified file."""
    soup = BeautifulSoup(f)
    # find all table rows
    for tr in soup.find('div', {'class': 'box-content'}).findAll('tr'):
        # find the rows with four columns of text
        tds = [
            clean(''.join(x.string for x in td.findAll(text=True)))
            for td in tr.findAll('td')
        ]
        if len(tds) >= 2 and tds[0] and tds[1]:
            yield tds[0], tds[1]
        if len(tds) >= 4 and tds[2] and tds[3]:
            yield tds[2], tds[3]


if __name__ == '__main__':
    headers = {
        'User-Agent': user_agent,
    }
    results = defaultdict(lambda: defaultdict(set))
    # read the states
    response = requests.get(state_list_url, headers=headers)
    for state, bps in parse(response.text):
        for bp in bps.split(','):
            results[bp.strip()]['state'] = state
            results[bp.strip()]['countries'].add('Malaysia')
    # read the countries
    response = requests.get(country_list_url, headers=headers)
    for country, bp in parse(response.text):
        results[bp]['countries'].add(country)
    # print the results
    print('# generated from National Registration Department of Malaysia, downloaded from')
    print('# %s' % state_list_url)
    print('# %s' % country_list_url)
    print('')
    for bp in sorted(results.iterkeys()):
        res = bp
        row = results[bp]
        if 'state' in row:
            res += ' state="%s"' % row['state']
        countries = list(row['countries'])
        countries.sort()
        if len(countries) == 1:
            res += ' country="%s"' % countries[0]
        if len(countries) > 0:
            res += ' countries="%s"' % (', '.join(countries))
        print(res)
