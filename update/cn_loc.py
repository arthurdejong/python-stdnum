#!/usr/bin/env python3

# update/cn_loc.py - script to fetch data from the CN Open Data community
#
# Copyright (C) 2014-2015 Jiangge Zhang
# Copyright (C) 2015-2025 Arthur de Jong
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

"""This downloads the birth place codes from from Wikipedia."""

import re
import unicodedata
from collections import defaultdict

import requests


# The wikipedia pages to download
wikipedia_pages = [f'中华人民共和国行政区划代码 ({i}区)' for i in range(1, 9)]


def get_wikipedia_url(page):
    """Get the Simplified Chinese Wikipedia page URL."""
    return f'https://zh.wikipedia.org/w/index.php?title={page.replace(" ", "_")}&action=raw'  # noqa: E231


# Regular expression for matching province heading
province_re = re.compile(r'^== *(?P<province>.*) +\((?P<prefix>[0-9]+)\) +==')

# Regular expression for matching table row
entry_re = re.compile(
    r'^\| *(?P<number>[0-9]{6}) *' +
    r'\|\| *(?P<activation>.*) *' +
    r'\|\| *(?P<revocation>.*) *' +
    r'\|\| *(?P<county>.*) *' +
    r'\|\| *(?P<code>.*)')


def clean(value):
    """Normalise (partially) unicode strings."""
    # Remove unicode parenthesis that include space with normal ones
    value = value.replace(
        unicodedata.lookup('FULLWIDTH LEFT PARENTHESIS'), ' (',
    ).replace(
        unicodedata.lookup('FULLWIDTH RIGHT PARENTHESIS'), ') ',
    )
    # Remove Wikipedia links
    return re.sub(r'\[\[([^]|]*\|)?([^]|]+)\]\]', r'\2', value)


def parse_county(county, activation, revocation):
    """Parse the county string and return ranges counties."""
    for value in county.split('<br>'):
        m = re.match(r'(?P<county>.*) +\((?P<year>[0-9]{4})年至今\) +', value)
        # This parses various formats as seen on Wikipedia
        if m:  # starting with year
            yield f'[{m.group("year")}-{revocation}]{m.group("county")}'
            continue
        m = re.match(r'(?P<county>.*) +\((?P<year>[0-9]{4})年前\) +', value)
        if m:  # before given year
            yield f'[{activation}-{int(m.group("year")) - 1}]{m.group("county")}'
            continue
        m = re.match(r'(?P<county>.*) +\((?P<years>[0-9]{4}-[0-9]{4})年曾撤销\) +', value)
        if m:  # abolished between years
            if activation or revocation:
                yield f'[{activation}-{revocation}]{m.group("county")}'
            else:
                yield m.group('county')
            continue
        m = re.match(r'(?P<county>.*) +\((?P<start>[0-9]{4})年?-(?P<end>[0-9]{4})年\) +', value)
        if m:
            yield f'[{m.group("start")}-{int(m.group("end")) - 1}]{m.group("county")}'
            continue
        if activation or revocation:
            yield f'[{activation}-{revocation}]{value}'
        else:
            yield value


def parse_page(content):
    """Parse the contents of the Wikipedia page and return number, county, province tuples."""
    province = None
    prefix = None
    for line in clean(content).splitlines():
        line = clean(line)
        m = province_re.match(line)
        if m:
            province = m.group('province')
            prefix = m.group('prefix')
            continue
        m = entry_re.match(line)
        if m:
            number = m.group('number')
            assert number.startswith(prefix)
            counties = m.group('county')
            try:
                activation = str(int(m.group('activation')))
            except ValueError:
                activation = ''
            try:
                revocation = str(int(m.group('revocation')))
            except ValueError:
                revocation = ''
            for county in parse_county(counties, activation, revocation):
                yield prefix, province, number, county.strip()


if __name__ == '__main__':
    """Output a data file in the right format."""
    print('# Downloaded from')
    for page in wikipedia_pages:
        print(f'# {get_wikipedia_url(page)}')
    # Download all data
    provinces = {}
    numbers = defaultdict(lambda: defaultdict(list))
    for page in wikipedia_pages:
        response = requests.get(get_wikipedia_url(page), timeout=30)
        response.raise_for_status()
        for prefix, province, number, county in parse_page(response.text):
            provinces[prefix] = province
            numbers[prefix][number].append(county)
    # Print data
    for prefix, province in sorted(provinces.items()):
        print(f'{prefix} province="{province}"')
        for number, counties in sorted(numbers[prefix].items()):
            county = ','.join(sorted(counties))
            print(f'  {number[2:]} county="{county}"')
