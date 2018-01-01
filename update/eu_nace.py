#!/usr/bin/env python3

# update/eu_nace.py - script to get the NACE v2 catalogue
#
# Copyright (C) 2017-2018 Arthur de Jong
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

import cgi
import urllib.request
from xml.etree import ElementTree


# the location of the ISBN Ranges XML file
download_url = 'http://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=ACT_OTH_CLS_DLD&StrNom=NACE_REV2&StrFormat=XML&StrLanguageCode=EN'


if __name__ == '__main__':
    f = urllib.request.urlopen(download_url)
    _, params = cgi.parse_header(f.info().get('Content-Disposition', ''))
    filename = params.get('filename', '?')
    print('# generated from %s, downloaded from' % filename)
    print('# %s' % download_url)

    # parse XML document
    doc = ElementTree.parse(f).getroot()

    # output header
    print('# %s: %s' % (
        doc.find('Classification').get('id'),
        doc.find('Classification/Label/LabelText[@language="EN"]').text))

    for item in doc.findall('Classification/Item'):
        number = item.get('id')
        level = int(item.get('idLevel', 0))
        label = item.find('Label/LabelText[@language="EN"]').text
        isic = item.find(
            'Property[@genericName="ISIC4_REF"]/PropertyQualifier/' +
            'PropertyText').text
        if level == 1:
            section = number
            print('%s label="%s" isic="%s"' % (number, label, isic))
        elif level == 2:
            print('%s section="%s" label="%s" isic="%s"' % (
                number, section, label, isic))
        else:
            print('%s%s label="%s" isic="%s"' % (
                ' ' * (level - 2), number[level], label, isic))
