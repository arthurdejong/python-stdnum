#!/usr/bin/env python

# getiban.py - script to donwload and parse data from the IBAN registry
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

"""This script downloads data from SWIFT (the Society for Worldwide Interbank
Financial Telecommunication which is the official IBAN registrar) to get
the data needed to correctly parse and validate IBANs."""

import urllib


# The place where the current version of IBAN_Registry.txt can be downloaded.
download_url = 'http://www.swift.com/dsp/resources/documents/IBAN_Registry.txt'


def splitlines(f):
    """Read lines from the TAB-delimited IBAN_Registry.txt file and return
    a dictionary per read line. We clean up the values a bit because it
    contains some junk."""
    stripit = ' \t\n\r;:\'"'
    firstline = [x.strip(stripit) for x in f.readline().lower().split('\t')]
    for line in f:
        yield dict(zip(firstline, [x.strip(stripit)
                                   for x in line.split('\t')]))


def get_country_codes(line):
    """Return the list of country codes this line has."""
    # simplest case first
    if len(line['country code as defined in iso 3166']) == 2:
        return [line['country code as defined in iso 3166']]
    # fall back to parsing the IBAN structure
    return [x.strip()[:2] for x in line['iban structure'].split(',')]


def parse(f):
    """Parse the specified file."""
    print '# generated from IBAN_Registry.txt, downloaded from'
    print '# %s' % download_url
    for line in splitlines(f):
        for cc in get_country_codes(line):
            # print country line
            print '%s country="%s" bban="%s"' % (
                cc, line['name of country'], line['bban structure'])
            # TODO: some countries have a fixed check digit value
            # TODO: some countries have extra check digits
            # TODO: use "Bank identifier position within the BBAN" field
            #       to add labels to the ranges (Bank identifier and Branch
            #       Identifier)


if __name__ == '__main__':
    #f = open('IBAN_Registry.txt', 'r')
    f = urllib.urlopen(download_url)
    parse(f)
