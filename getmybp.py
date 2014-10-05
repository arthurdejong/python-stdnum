#!/usr/bin/env python

# getmybp.py - script to donwnload data from Malaysian government site
#
# Copyright (C) 2013 Arthur de Jong
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

from collections import defaultdict
import re
import urllib

import BeautifulSoup


# URLs that are downloaded
state_list_url = 'http://www.jpn.gov.my/informasi/kod-negeri/'
country_list_url = 'http://www.jpn.gov.my/en/informasi/kod-negara/'


spaces_re = re.compile('\s+', re.UNICODE)


def clean(s):
    """Cleans up the string removing unneeded stuff from it."""
    return spaces_re.sub(' ', s.replace(u'\u0096', '')).strip().encode('utf-8')


def parse(f):
    """Parse the specified file."""
    soup = BeautifulSoup.BeautifulSoup(f, convertEntities='html')
    # find all table rows
    for tr in soup.find('div', id='inner-main').findAll('tr'):
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
    results = defaultdict(lambda : defaultdict(set))
    # read the states
    #f = open('/tmp/states.html', 'r')
    f = urllib.urlopen(state_list_url)
    for state, bps in parse(f):
        for bp in bps.split(','):
            results[bp.strip()]['state'] = state
            results[bp.strip()]['countries'].add('Malaysia')
    # read the countries
    #f = open('/tmp/countries.html', 'r')
    f = urllib.urlopen(country_list_url)
    for country, bp in parse(f):
        results[bp]['countries'].add(country)
    # print the results
    print '# generated from National Registration Department of Malaysia, downloaded from'
    print '# %s' % state_list_url
    print '# %s' % country_list_url
    print
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
        print res
