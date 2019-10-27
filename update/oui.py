#!/usr/bin/env python3

# update/oui.py - script to download and parse data from the IEEE registry
#
# Copyright (C) 2018-2019 Arthur de Jong
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

"""This script downloads data from the IEEE web site
https://regauth.standards.ieee.org/standards-ra-web/pub/view.html
and produces data files that can be use by python-stdnum to look up
manufacturers by MAC address."""

import csv
from collections import defaultdict
from itertools import chain

import requests


# The URLs of the MA-L, MA-M and MA-S registries that are downloaded to
# construct a full list of manufacturer prefixes.
mal_url = 'http://standards-oui.ieee.org/oui/oui.csv'
mam_url = 'http://standards-oui.ieee.org/oui28/mam.csv'
mas_url = 'http://standards-oui.ieee.org/oui36/oui36.csv'


def download_csv(url):
    """Download the list from the site and provide assignment and
    organisation names."""
    response = requests.get(url)
    response.raise_for_status()
    for row in csv.DictReader(line.decode('utf-8') for line in response.iter_lines()):
        o = row['Organization Name'].strip().replace('"', '%')
        if o not in ('IEEE Registration Authority', 'Private'):
            yield (row['Assignment'], o)


def join_items(items):
    """Join the list of items, combining consecutive numbers."""
    length = len(items[0])
    items = [int(b, 16) for b in items]
    first = None
    prev = None
    res = ''
    for item in items:
        if first is not None and item == prev + 1:
            # this item is consecutive to the previous: make a range
            if prev > first:
                # replace the previous value
                res = res[:-length - 1]
            res += '-%%0%dX' % length % item
            prev = item
        else:
            # this is a new item, add a new one to the list
            res += ',%%0%dX' % length % item
            first = prev = item
    return res.strip(',')


if __name__ == '__main__':
    # download the MAC Address Block Large (MA-L) list and group by org
    toplevel = defaultdict(list)
    for a, o in download_csv(mal_url):
        toplevel[o].append(a)
    # download the MAC Address Block Medium (MA-M) and Small lists
    nested = defaultdict(dict)
    for a, o in chain(download_csv(mam_url), download_csv(mas_url)):
        nested[a[:6]][a[6:]] = o
    # Generate output
    print('# list of IEEE MAC Address Block registry entries')
    print('# %s' % mal_url)
    print('# %s' % mam_url)
    print('# %s' % mas_url)
    # output full-length assignments
    for a, o in sorted((tuple(sorted(a)), o) for o, a in toplevel.items()):
        print('%s o="%s"' % (join_items(a), o))
    # output assignments that are subdivided
    for a in sorted(nested.keys()):
        print('%s' % a)
        for s, o in sorted(nested[a].items()):
            print(' %s o="%s"' % (s, o))
