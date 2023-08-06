#!/usr/bin/env python3

# check_headers.py - check that all source files have licensing information
#
# Copyright (C) 2023 Arthur de Jong
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

"""This script checks that all source files have licensing information."""

import glob
import os
import re
import sys
import textwrap


# Regext to match the first line
identification_re = re.compile(
    r'^(#!/usr/bin/env python3?\s+|/\*\s+)?'
    r'(# coding: utf-8\s+)?'
    r'(\s?#\s+)?'
    r'(?P<filename>[^ :]+) - ', re.MULTILINE)

# Regex to match standard license blurb
license_re = re.compile(textwrap.dedent(r'''
    [# ]*This library is free software; you can redistribute it and/or
    [# ]*modify it under the terms of the GNU Lesser General Public
    [# ]*License as published by the Free Software Foundation; either
    [# ]*version 2.1 of the License, or .at your option. any later version.
    [# ]*
    [# ]*This library is distributed in the hope that it will be useful,
    [# ]*but WITHOUT ANY WARRANTY; without even the implied warranty of
    [# ]*MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    [# ]*Lesser General Public License for more details.
    [# ]*
    [# ]*You should have received a copy of the GNU Lesser General Public
    [# ]*License along with this library; if not, write to the Free Software
    [# ]*Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
    [# ]*02110-1301 USA
    ''').strip(), re.MULTILINE)


def get_file_header(filename):
    """Read the file header from the file."""
    with open(filename, 'rt') as f:
        # Only read the first 2048 bytes to avoid loading too much and the
        # license information should be in the first part anyway.
        return f.read(2048)


if __name__ == '__main__':
    files_to_check = (
        glob.glob('*.py') +
        glob.glob('stdnum/**/*.py', recursive=True) +
        glob.glob('tests/**/*.doctest', recursive=True) +
        glob.glob('scripts/*', recursive=True) +
        glob.glob('update/**/*.py', recursive=True) +
        glob.glob('online_check/*.wsgi', recursive=True) +
        glob.glob('online_check/check.js', recursive=True)
    )

    # Look for files with incorrect first lines or license
    fail = False
    for filename in sorted(files_to_check):
        contents = get_file_header(filename)
        m = identification_re.match(contents)
        if not bool(m) or m.group('filename') not in (filename, os.path.basename(filename)):
            print('%s: Incorrect file identification' % filename)
            fail = True
        if not bool(license_re.search(contents)):
            print('%s: Incorrect license text' % filename)
            fail = True

    if fail:
        sys.exit(1)
