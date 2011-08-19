#!/usr/bin/env python

# getisbn.py - script to get ISBN prefix data
#
# Copyright (C) 2010, 2011 Arthur de Jong
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

import xml.sax
import urllib


# The place where the current version of RangeMessage.xml can be downloaded.
download_url = 'http://www.isbn-international.org/agency?rmxml=1'


def _wrap(text):
    """Generator that returns lines of text that are no longer than
    max_len."""
    while text:
        i = len(text)
        if i > 73:
            i = text.rindex(',', 20, 73)
        yield text[:i]
        text = text[i + 1:]


class RangeHandler(xml.sax.ContentHandler):

    def __init__(self):
        self._gather = None
        self._prefix = None
        self._agency = None
        self._range = None
        self._length = None
        self._ranges = []
        self._last = None
        self._topranges = {}

    def startElement(self, name, attrs):
        if name in ('MessageSerialNumber', 'MessageDate', 'Prefix',
                    'Agency', 'Range', 'Length'):
            self._gather = ''

    def characters(self, content):
        if self._gather is not None:
            self._gather += content

    def endElement(self, name):
        if name == 'MessageSerialNumber':
            print '# file serial %s' % self._gather.strip()
        elif name == 'MessageDate':
            print '# file date %s' % self._gather.strip()
        elif name == 'Prefix':
            self._prefix = self._gather.strip()
        elif name == 'Agency':
            self._agency = self._gather.strip()
        elif name == 'Range':
            self._range = self._gather.strip()
        elif name == 'Length':
            self._length = int(self._gather.strip())
        elif name == 'Rule' and self._length:
            self._ranges.append(tuple(x[:self._length]
                                      for x in self._range.split('-')))
        elif name == 'Rules':
            if '-' in self._prefix:
                p, a = self._prefix.split('-')
                if p != self._last:
                    print p
                    self._last = p
                    for line in _wrap(','.join(r[0] + '-' + r[1]
                                               for r in self._topranges[p])):
                        print ' %s' % line
                print ' %s agency="%s"' % (a, self._agency)
                for line in _wrap(','.join(r[0] + '-' + r[1]
                                           for r in self._ranges)):
                    print '  %s' % line
            else:
                self._topranges[self._prefix] = self._ranges
            self._ranges = []
        self._gather = None


if __name__ == '__main__':
    print '# generated from RangeMessage.xml, downloaded from'
    print '# %s' % download_url
    parser = xml.sax.make_parser()
    parser.setContentHandler(RangeHandler())
    parser.parse(urllib.urlopen(download_url))
    #parser.parse('RangeMessage.xml')
