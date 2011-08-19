#!/usr/bin/env python

# getisil.py - script to donwload ISIL agencies
#
# Copyright (C) 2011 Arthur de Jong
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

"""This script downloads a web page from the ISIL Registration Authority
and screen-scrapes the national and non-national ISIL agencies and
code prefixes."""

import urllib
import BeautifulSoup
import re

spaces_re = re.compile('\s+', re.UNICODE)

# the web page that holds information on the ISIL authorities
download_url = 'http://biblstandard.dk/isil/'


def clean(s):
    """Cleans up the string removing unneeded stuff from it."""
    return spaces_re.sub(' ', s.replace(u'\u0096', '')).strip().encode('utf-8')


def parse(f):
    """Parse the specified file."""
    print '# generated from ISIL Registration Authority, downloaded from'
    print '# %s' % download_url
    soup = BeautifulSoup.BeautifulSoup(f, convertEntities='html')
    # find all table rows
    for tr in soup.findAll('tr'):
        # find the rows with four columns of text
        tds = tr.findAll('td', attrs={'class': 'text'}, recursive=False)
        if len(tds) == 4:
            props = {}
            cc = clean(tds[0].string)
            if tds[1].string:
                props['country'] = clean(tds[1].contents[0])
            ra_a = tds[2].find('a')
            if ra_a:
                props['ra'] = clean(ra_a.string)
                props['ra_url'] = clean(ra_a['href'])
            elif tds[2].string:
                props['ra'] = clean(tds[2].string)
            # we could also get the search urls from tds[3].findAll('a')
            print '%s$ %s' % (
                      cc,
                      ' '.join(['%s="%s"' % (x, y)
                                for x, y in props.iteritems()]))


if __name__ == '__main__':
    #f = open('isil.html', 'r')
    f = urllib.urlopen(download_url)
    parse(f)
