#!/usr/bin/env python

# getismsi.py - script to donwload data from Wikipedia to build the database
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

import urllib
import re


# URLs that are downloaded
mcc_list_url = 'http://en.wikipedia.org/w/index.php?title=List_of_mobile_country_codes&action=raw'
mnc_list_url = 'http://en.wikipedia.org/w/index.php?title=Mobile_Network_Code&action=raw'


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


def cleanup_value(val):
    """Remove unneeded markup from the value."""
    # remove uninteresting things from value
    val = val.replace('[', '').replace(']', '').strip()
    # replace value
    val = val.replace('United Kingdom|UK', 'United Kingdom')
    val = val.replace('United States|US', 'United States')
    val = val.replace('New Zealand|NZ', 'New Zealand')
    return cleanup_replacements.get(val, val)


def update_mccs(mccs, mcc, **kwargs):
    """Merge provided information in kwrags with the already stored
    information in mccs."""
    if mcc not in mccs:
        mccs[mcc] = dict()
    mccs[mcc].update(dict((k, cleanup_value(v)) for k,v in kwargs.items() if v))


def update_mncs(mccs, mcc, mnc, **kwargs):
    """Merge provided mnc information with the data that is already stored
    in mccs."""
    if mcc not in mccs:
        mccs[mcc] = dict()
    mncs = mccs[mcc]
    if mnc not in mncs:
        mncs[mnc] = dict()
    mncs[mnc].update(dict((k, cleanup_value(v)) for k,v in kwargs.items() if v))


def get_mccs_from_wikipedia(mccs):
    """Returns a dictionary of Mobile Country Codes mapping to a dictionary
    that holds the cc (country code) and country (country name) keys. This
    function parses a Wikipedia page."""
    mcc_line_re = re.compile('^\|\s*(?P<mcc>[0-9]+)\s*\|\|\s*(?P<cc>[^\s]+)\s*\|\|\s*(?P<country>.*)\s*$')
    f = urllib.urlopen(mcc_list_url)
    for line in f.readlines():
        # search for lines that are part of the table
        match = mcc_line_re.search(line)
        if match:
            update_mccs(mccs, match.group('mcc'), cc=match.group('cc').lower(),
                        country=match.group('country'))


def get_mncs_from_itu(mccs):
    """This parses a text file that contains the copy-pasted table from the
    "Mobile Network Codes (MNC) for the international identification plan
    for public networks and subscriptions" document by the
    TELECOMMUNICATION STANDARDIZATION BUREAU OF ITU downloaded from
    http://www.itu.int/itu-t/bulletin/annex.html"""
    twonumbers_re = re.compile('^\s*(?P<mcc>[0-9]+)\s+(?P<mnc>[0-9]+)\s*$')
    f = open('imsi.info', 'r')
    country = operator = ''
    for line in f.readlines():
        line = line.strip()
        if not line:
            country = operator
        else:
            match = twonumbers_re.search(line)
            if not match:
                operator = line
            else:
                update_mncs(mccs, match.group('mcc'), match.group('mnc'),
                            country=country, operator=operator)


def get_mncs_from_wikipedia(mccs):
    """Returns a dictionary of Mobile Country Codes mapping to a dictionary
    that holds the cc (country code) and country (country name) keys. This
    function parses a Wikipedia page."""
    mnc_country_re = re.compile('^====\s+(?P<country>.*?)(\s+-\s+(?P<cc>[^\s]{2}))?\s+====$')
    mnc_line_re = re.compile('^\|\s+(?P<mcc>[0-9]+)\s+\|\|\s+(?P<mnc>[0-9]+)' +
                             '(\s+\|\|\s+(?P<brand>[^|]*)' +
                             '(\s+\|\|\s+(?P<operator>[^|]*)' +
                             '(\s+\|\|\s+(?P<status>[^|]*)' +
                             '(\s+\|\|\s+(?P<bands>[^|]*)' + '))))')
    f = urllib.urlopen(mnc_list_url)
    country = cc = ''
    for line in f.readlines():
        line = line.strip()
        match = mnc_country_re.match(line)
        if match:
            country = match.group('country')
            cc = (match.group('cc') or '').lower()
        match = mnc_line_re.match(line)
        if match:
            update_mncs(mccs, match.group('mcc'), match.group('mnc'),
                        country=country, cc=cc, brand=match.group('brand'),
                        operator=match.group('operator'),
                        status=match.group('status'),
                        bands=match.group('bands'))


if __name__ == '__main__':
    # download/parse the information
    mccs_info = {}
    get_mccs_from_wikipedia(mccs_info)
    mccs_mncs_info = {}
    get_mncs_from_itu(mccs_mncs_info)
    get_mncs_from_wikipedia(mccs_mncs_info)
    # print header
    print '# generated from various sources'
    print '# %s' % mcc_list_url
    print '# %s' % mnc_list_url
    print '# http://www.itu.int/itu-t/bulletin/annex.html'
    # build an ordered list of mccs
    mccs = list(set(mccs_info.keys() + mccs_mncs_info.keys()))
    mccs.sort()
    # go over mccs
    for mcc in mccs:
        mcci = mccs_info.get(mcc, {})
        cc = mcci.get('cc', '')
        country = mcci.get('country', None)
        print '%s%s%s' % ( mcc, ' cc="%s"' % cc if cc else '',
                           ' country="%s"' % country if country else '')
        # build an ordered list of mncs
        mncs = mccs_mncs_info.get(mcc, {}).keys()
        mncs.sort()
        for mnc in mncs:
            info = mccs_mncs_info[mcc][mnc]
            if cc and info.get('cc', '') == cc:
                del info['cc']
            if country and info.get('country', None) == country:
                del info['country']
            infokeys = info.keys()
            infokeys.sort()
            print ' %s%s' % (mnc, ''.join([' %s="%s"' % (k, info[k]) for k in infokeys]))
        # try to get the length of mnc's
        try:
            l = len(mncs[0])
            print ' %s-%s' % (l * '0', l * '9')
        except IndexError:
            pass  # ignore
