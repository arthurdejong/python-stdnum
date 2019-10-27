#!/usr/bin/env python3

# update/eu_nace.py - script to get the NACE v2 catalogue
#
# Copyright (C) 2017-2019 Arthur de Jong
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

import re

import lxml.etree
import requests


# the location of the Statistical Classification file
download_url = 'https://ec.europa.eu/eurostat/ramon/nomenclatures/index.cfm?TargetUrl=ACT_OTH_CLS_DLD&StrNom=NACE_REV2&StrFormat=XML&StrLanguageCode=EN'


if __name__ == '__main__':
    response = requests.get(download_url)
    response.raise_for_status()
    content_disposition = response.headers.get('content-disposition', '')
    filename = re.findall(r'filename=?(.+)"?', content_disposition)[0].strip('"')
    print('# generated from %s, downloaded from' % filename)
    print('# %s' % download_url)

    # parse XML document
    document = lxml.etree.fromstring(response.content)

    # output header
    print('# %s: %s' % (
        document.find('./Classification').get('id'),
        document.find('./Classification/Label/LabelText[@language="EN"]').text))

    for item in document.findall('./Classification/Item'):
        number = item.get('id')
        level = int(item.get('idLevel', 0))
        label = item.find('./Label/LabelText[@language="EN"]').text
        isic = item.find(
            './Property[@genericName="ISIC4_REF"]/PropertyQualifier/PropertyText').text
        if level == 1:
            section = number
            print('%s label="%s" isic="%s"' % (number, label, isic))
        elif level == 2:
            print('%s section="%s" label="%s" isic="%s"' % (
                number, section, label, isic))
        else:
            print('%s%s label="%s" isic="%s"' % (
                ' ' * (level - 2), number[level], label, isic))
