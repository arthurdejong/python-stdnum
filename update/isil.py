#!/usr/bin/env python3

# update/isil.py - script to download ISIL agencies
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

"""This script downloads a web page from the ISIL Registration Authority
and screen-scrapes the national and non-national ISIL agencies and
code prefixes."""

import re

import lxml.html
import requests


spaces_re = re.compile(r'\s+', re.UNICODE)

# the web page that holds information on the ISIL authorities
download_url = 'https://slks.dk/english/work-areas/libraries-and-literature/library-standards/isil'


def clean(td):
    """Clean up the element removing unneeded stuff from it."""
    s = lxml.html.tostring(td, method='text', encoding='utf-8').decode('utf-8')
    return spaces_re.sub(' ', s.replace(u'\u0096', '')).strip()


if __name__ == '__main__':
    response = requests.get(download_url, timeout=30)
    response.raise_for_status()
    print('# generated from ISIL Registration Authority, downloaded from')
    print('# %s' % download_url)
    # We hack the HTML to insert missing <TR> elements
    content = response.text.replace('</TR>', '</TR><TR>')
    document = lxml.html.document_fromstring(content)
    # find all table rows
    for tr in document.findall('.//tr'):
        # find the rows with four columns of text
        tds = tr.findall('td')
        if len(tds) == 4 and clean(tds[0]).lower() != 'code':
            props = {}
            cc = clean(tds[0])
            if tds[1].find('p') is not None:
                props['country'] = clean(tds[1])
            ra_a = tds[2].find('.//a')
            if ra_a is not None:
                props['ra'] = clean(tds[2])
                props['ra_url'] = ra_a.get('href')
            else:
                props['ra'] = clean(tds[2])
            print(
                '%s$ %s' % (
                    cc, ' '.join(
                        '%s="%s"' % (x, y) for x, y in sorted(props.items()))))
