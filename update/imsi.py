#!/usr/bin/env python

# update/imsi.py - script to donwload from Wikipedia to build the database
#
# Copyright (C) 2011-2018 Arthur de Jong
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

"""This extracts a IMSI country and operator code from Wikipedia."""

import re
import urllib
from collections import defaultdict


# URLs that are downloaded
mcc_list_url = 'https://en.wikipedia.org/w/index.php?title=Mobile_country_code&action=raw'


cleanup_replacements = {
    'Anguilla (United Kingdom)': 'Anguilla',
    'Argentina|Argentine Republic': 'Argentina',
    'Aruba (Kingdom of the Netherlands|Netherlands)': 'Aruba',
    'Azerbaijan|Azerbaijani Republic': 'Azerbaijan',
    'Bermuda       (United Kingdom)': 'Bermuda',
    'British Virgin Islands (United Kingdom)': 'British Virgin Islands',
    'Brunei|Brunei Darussalam': 'Brunei',
    'Cayman Islands': 'Cayman Islands (United Kingdom)',
    'Cayman Islands (United Kingdom)': 'Cayman Islands (United Kingdom)',
    'Czech Rep.': 'Czech Republic',
    'Democratic People\'s Republic of Korea|Korea, North': 'North Korea',
    'Denmark (Kingdom of Denmark)': 'Denmark',
    'Faroe Islands (Kingdom of Denmark)': 'Faroe Islands (Denmark)',
    'French Polynesia (France)': 'French Polynesia',
    'Gabon|Gabonese Republic': 'Gabon',
    'Georgia (country)|Georgia': 'Georgia',
    'Gibraltar': 'Gibraltar (United Kingdom)',
    'Gibraltar (United Kingdom)': 'Gibraltar (United Kingdom)',
    'Greenland (Kingdom of Denmark)': 'Greenland (Denmark)',
    'Guadeloupe': 'Guadeloupe (France)',
    'Hong Kong (People\'s Republic of China|PRC)': 'Hong Kong (China)',
    'Hong Kong (Special Administrative Region of People\'s Republic of China)': 'Hong Kong (China)',
    'Korea (Rep. of)': 'South Korea',
    'Kyrgyz Republic': 'Kyrgyzstan',
    'Lao People\'s Democratic Republic|Laos': 'Laos',
    'Macau (People\'s Republic of China)': 'Macau (China)',
    'Macau (People\'s Republic of China|PRC)': 'Macau (China)',
    'Martinique': 'Martinique (France)',
    'Moldova (Republic of)': 'Moldova',
    'Montenegro (Republic of)': 'Montenegro',
    'Netherlands (Kingdom of the Netherlands)': 'Netherlands',
    'Palestinian Authority': 'Palestinian territories',
    'Palestinian territories|Palestine': 'Palestinian territories',
    'People\'s Republic of China|China': 'China',
    'Puerto Rico (United States)': 'Puerto Rico',
    'Republic of Ireland|Ireland': 'Ireland',
    'Republic of Korea|Korea, South': 'South Korea',
    'Russian Federation': 'Russian Federation',
    'Rwanda|Rwandese Republic': 'Rwanda',
    'Serbia (Republic of)': 'Serbia',
    'Somali Democratic Republic|Somalia': 'Somalia',
    'Syrian Arab Republic': 'Syria',
    'Syrian Arab Republic|Syria': 'Syria',
    'Turks and Caicos Islands (United Kingdom)': 'Turks and Caicos Islands',
    'United States': 'United States of America',
    'United States Virgin Islands (United States)': 'United States Virgin Islands',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Vietnam|Viet Nam': 'Vietnam',
}


remove_ref_re = re.compile(r'<ref>.*?</ref>')
remove_comment_re = re.compile(r'{{.*?}}')
quotes = u'\xab\xbb\u201c\u201d\u2018\u2019'
remove_href_re = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+' +
                            r'[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|' +
                            r'(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|' +
                            r'(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>' +
                            r'?' + quotes + ']))')


def cleanup_value(val):
    """Remove unneeded markup from the value."""
    # remove uninteresting things from value
    val = remove_comment_re.sub('', val)
    val = remove_ref_re.sub('', val)
    val = remove_href_re.sub('', val)
    val = val.replace('[', '').replace(']', '').replace('\'\'', '').strip()
    val = val.split('|')[-1]
    # replace value
    val = val.replace('Unknown', '')
    val = val.replace('United Kingdom|UK', 'United Kingdom')
    val = val.replace('United States|US', 'United States')
    val = val.replace('New Zealand|NZ', 'New Zealand').strip()
    return cleanup_replacements.get(val, val)


def update_mncs(data, mcc, mnc, **kwargs):
    """Merge provided mnc information with the data that is already stored
    in mccs."""
    data[mcc][mnc].update(dict((k, cleanup_value(v)) for k, v in kwargs.items() if v))


def get_mncs_from_wikipedia(data):
    """Update the collection of Mobile Country Codes from Wikipedia.
    This parses a Wikipedia page to extract the MCC and MNC, the first
    part of any IMSI, and stores the results."""
    mnc_country_re = re.compile(r'^[=]{2,4}\s+(?P<country>.*?)(\s+-\s+(?P<cc>[^\s]{2}))?\s+[=]{2,4}$')
    mnc_line_re = re.compile(r'^\|\s*(?P<mcc>[0-9]+)' +
                             r'\s*\\\\\s*(?P<mnc>[0-9]+)' +
                             r'(\s*\\\\\s*(?P<brand>[^\\]*)' +
                             r'(\s*\\\\\s*(?P<operator>[^\\]*)' +
                             r'(\s*\\\\\s*(?P<status>[^\\]*)' +
                             r'(\s*\\\\\s*(?P<bands>[^\\]*)' +
                             r'(\s*\\\\\s*(?P<notes>[^\\]*)' +
                             r')?)?)?)?)?')
    f = urllib.urlopen(mcc_list_url)
    country = cc = ''
    for line in f.readlines():
        line = line.strip()
        match = mnc_country_re.match(line)
        if match:
            country = match.group('country')
            cc = (match.group('cc') or '').lower()
        if '||' not in line:
            continue
        line = line.replace('||', '\\\\')
        match = mnc_line_re.match(line)
        if match:
            for mnc in str2range(match.group('mnc')):
                update_mncs(data, match.group('mcc'), mnc,
                            country=country, cc=cc, brand=match.group('brand'),
                            operator=match.group('operator'),
                            status=match.group('status'),
                            bands=match.group('bands'))


def str2range(x):
    """Convert the comma-separated list of ranges to a list of numbers."""
    result = []
    for part in x.split(','):
        if '-' in part:
            a, b = part.split('-')
            f = '%0' + str(len(b)) + 'd'
            a, b = int(a), int(b)
            for i in range(a, b + 1):
                result.append(f % (i))
        else:
            result.append(part)
    return result


if __name__ == '__main__':
    # download/parse the information
    data = defaultdict(lambda: defaultdict(dict))
    get_mncs_from_wikipedia(data)
    # print header
    print('# generated from various sources')
    print('# %s' % mcc_list_url)
    # build an ordered list of mccs
    mcc_list = list(data.keys())
    mcc_list.sort()
    # go over mccs
    for mcc in mcc_list:
        print('%s' % mcc)
        # build an ordered list of mncs
        mnc_list = data[mcc].keys()
        mnc_list.sort()
        for mnc in mnc_list:
            info = data[mcc][mnc]
            infokeys = info.keys()
            infokeys.sort()
            print(' %s%s' % (mnc, ''.join([' %s="%s"' % (k, info[k]) for k in infokeys if info[k]])))
        # try to get the length of mnc's
        try:
            length = len(mnc_list[0])
            if all(len(x) == length for x in mnc_list):
                print(' %s-%s' % (length * '0', length * '9'))
        except IndexError:
            pass  # ignore
