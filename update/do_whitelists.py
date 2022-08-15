#!/usr/bin/env python3
# coding: utf-8

# update/do_whitelists.py - script to update do.rnc and do.cedula whitelists
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

"""This script downloads a ZIP file from the Dirección General de Impuestos
Internos (DGII) web site with lists of all RNC and Cedula values and outputs
new whitelists for these modules."""

import io
import os.path
import sys
import tempfile
import textwrap
import zipfile

import requests


# Ensure that our local stdnum implementation is used
sys.path.insert(0, os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))

from stdnum.do import cedula, rnc  # noqa, isort:skip


# The URL of the zip file with all valid numbers
download_url = 'https://www.dgii.gov.do/app/WebApps/Consultas/rnc/DGII_RNC.zip'


def handle_zipfile(f):
    """Parse the ZIP file and return a set of invalid RNC and Cedula."""
    # collections of invalid numbers found
    invalidrnc = set()
    invalidcedula = set()
    # read the information from the ZIP file
    z = zipfile.ZipFile(f, 'r')
    for line in io.TextIOWrapper(z.open('TMP/DGII_RNC.TXT'), encoding='iso8859-15'):
        number = line.split('|', 1)[0].strip()
        if number.isdigit():
            if len(number) <= 9:
                if not rnc.is_valid(number):
                    invalidrnc.add(number)
            else:
                if not cedula.is_valid(number):
                    invalidcedula.add(number)
    # return known but invalid numbers
    return invalidrnc, invalidcedula


if __name__ == '__main__':

    # Download and read the ZIP file with valid data
    with tempfile.TemporaryFile() as tmp:
        # Download the zip file to a temporary file
        response = requests.get(download_url, stream=True, timeout=30)
        response.raise_for_status()
        print('%s: %s' % (
            os.path.basename(download_url),
            response.headers.get('last-modified')))
        tmp.write(response.content)
        # Open the temporary file as a zip file and read contents
        # (we cannot do this streaming because zipfile requires seek)
        invalidrnc, invalidcedula = handle_zipfile(tmp)

    # Output new RNC whitelist if changed
    if not invalidrnc:
        print('NO NEW WHITELISTED RNC')
    else:
        print('NEW RNC WHITELIST:')
        print('\n'.join(textwrap.wrap(
            ' '.join(sorted(rnc.whitelist | invalidrnc)), 77)))

    # Output new Cedula whitelist if changed
    if not invalidrnc:
        print('NO NEW WHITELISTED CEDULA')
    else:
        print('NEW CEDULA WHITELIST:')
        print('\n'.join(textwrap.wrap(
            ' '.join(sorted(cedula.whitelist | invalidcedula)), 77)))
