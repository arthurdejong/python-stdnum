#!/usr/bin/env python

# getisbn.py - script to get ISBN prefix data
#
# Copyright (C) 2010, 2011, 2014 Arthur de Jong
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

from xml.etree import ElementTree
import urllib


# the location of the ISBN Ranges XML file
download_url = 'https://www.isbn-international.org/export_rangemessage.xml'


def ranges(group):
    for rule in group.find('Rules').findall('Rule'):
        length = int(rule.find('Length').text.strip())
        if length:
            yield '-'.join(
                x[:length]
                for x in rule.find('Range').text.strip().split('-'))


def wrap(text):
    while text:
        i = len(text)
        if i > 73:
            i = text.rindex(',', 20, 73)
        yield text[:i]
        text = text[i + 1:]


def get(f=None):
    if f is None:
        yield '# generated from RangeMessage.xml, downloaded from'
        yield '# %s' % download_url
        f = urllib.urlopen(download_url)
    else:
        yield '# generated from %r' % f

    # parse XML document
    msg = ElementTree.parse(f).getroot()

    # dump data from document
    yield '# file serial %s' % msg.find('MessageSerialNumber').text.strip()
    yield '# file date %s' % msg.find('MessageDate').text.strip()

    top_groups = dict(
        (x.find('Prefix').text.strip(), x)
        for x in msg.find('EAN.UCCPrefixes').findall('EAN.UCC'))

    prevtop = None
    for group in msg.find('RegistrationGroups').findall('Group'):
        top, prefix = group.find('Prefix').text.strip().split('-')
        agency = group.find('Agency').text.strip()
        if top != prevtop:
            yield top
            for line in wrap(','.join(ranges(top_groups[top]))):
                yield ' %s' % line
            prevtop = top
        yield ' %s agency="%s"' % (prefix, agency)
        for line in wrap(','.join(ranges(group))):
            yield '  %s' % line


if __name__ == '__main__':
    # get('RangeMessage.xml')
    for row in get():
        print row.encode('utf-8')
