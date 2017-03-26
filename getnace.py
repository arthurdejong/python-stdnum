#!/usr/bin/env python3

# getnace.py - script to get the NACE v2 catalogue
#
# Copyright (C) 2017 Arthur de Jong
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

"""This script downloads XML data from the European commission RAMON Eurostat
Metadata Server and extracts the information that is used for validating NACE
codes."""

from xml.etree import ElementTree
import cgi
import urllib.request


# the location of the ISBN Ranges XML file
download_url = 'http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=ACT_OTH_CLS_DLD&StrNom=NACE_REV2&StrFormat=XML&StrLanguageCode=EN'


def get(f=None):
    if f is None:
        f = urllib.request.urlopen(download_url)
        _, params = cgi.parse_header(f.info().get('Content-Disposition', ''))
        filename = params.get('filename', '?')
        yield '# generated from %s, downloaded from' % filename
        yield '# %s' % download_url
    else:
        yield '# generated from %s' % f

    # parse XML document
    doc = ElementTree.parse(f).getroot()

    # output header
    yield '# %s: %s' % (
        doc.find('Classification').get('id'),
        doc.find('Classification/Label/LabelText[@language="EN"]').text)

    for item in doc.findall('Classification/Item'):
        number = item.get('id')
        level = int(item.get('idLevel', 0))
        label = item.find('Label/LabelText[@language="EN"]').text
        isic = item.find(
            'Property[@genericName="ISIC4_REF"]/PropertyQualifier/' +
            'PropertyText').text
        if level == 1:
            section = number
            yield '%s label="%s" isic="%s"' % (number, label, isic)
        elif level == 2:
            yield '%s section="%s" label="%s" isic="%s"' % (
                number, section, label, isic)
        else:
            yield '%s%s label="%s" isic="%s"' % (
                ' ' * (level - 2), number[level], label, isic)


if __name__ == '__main__':
    #get('NACE_REV2_20170326_162216.xml')
    for row in get():
        print(row)
