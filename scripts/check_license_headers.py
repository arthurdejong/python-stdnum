#!/usr/bin/env python3

# check_license_headers - check that all source files have licensing information
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
import re
import sys
import textwrap


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


def file_has_correct_license(filename):
    """Check that the file contains a valid license header."""
    with open(filename, 'rt') as f:
        # Only read the first 2048 bytes to avoid loading too much and the
        # license information should be in the first part anyway.
        contents = f.read(2048)
        return bool(license_re.search(contents))


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

    incorrect_files = [f for f in files_to_check if not file_has_correct_license(f)]
    if incorrect_files:
        print('Files with incorrect license information:')
        print('\n'.join(incorrect_files))
        sys.exit(1)
