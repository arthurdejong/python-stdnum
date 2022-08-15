#!/usr/bin/env python3

# update/isbn.py - script to get ISBN prefix data
#
# Copyright (C) 2010-2019 Arthur de Jong
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

"""This script downloads XML data from the International ISBN Agency
website and provides a compact form of all group prefixes, and registrant
ranges for those prefixes suitable for the numdb module. This data is needed
to correctly split ISBNs into an EAN.UCC prefix, a group prefix, a registrant,
an item number and a check-digit."""

import lxml.etree
import requests


# the location of the ISBN Ranges XML file
download_url = 'https://www.isbn-international.org/export_rangemessage.xml'


def ranges(group):
    """Provide the ranges for the group."""
    for rule in group.findall('./Rules/Rule'):
        length = int(rule.find('./Length').text.strip())
        if length:
            yield '-'.join(
                x[:length]
                for x in rule.find('./Range').text.strip().split('-'))


def wrap(text):
    """Rewrap the provided text into lines."""
    while text:
        i = len(text)
        if i > 73:
            i = text.rindex(',', 20, 73)
        yield text[:i]
        text = text[i + 1:]


if __name__ == '__main__':
    print('# generated from RangeMessage.xml, downloaded from')
    print('# %s' % download_url)
    response = requests.get(download_url, timeout=30)
    response.raise_for_status()

    # parse XML document
    document = lxml.etree.fromstring(response.content)

    # dump data from document
    print('# file serial %s' % document.find('./MessageSerialNumber').text.strip())
    print('# file date %s' % document.find('./MessageDate').text.strip())

    top_groups = dict(
        (x.find('./Prefix').text.strip(), x)
        for x in document.findall('./EAN.UCCPrefixes/EAN.UCC'))

    prevtop = None
    for group in document.findall('./RegistrationGroups/Group'):
        top, prefix = group.find('./Prefix').text.strip().split('-')
        agency = group.find('./Agency').text.strip()
        if top != prevtop:
            print(top)
            for line in wrap(','.join(ranges(top_groups[top]))):
                print(' %s' % line)
            prevtop = top
        print(' %s agency="%s"' % (prefix, agency))
        for line in wrap(','.join(ranges(group))):
            print('  %s' % line)
