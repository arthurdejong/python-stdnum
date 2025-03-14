# test_eu_excise.py - functions for testing the online SEED validation
# coding: utf-8
#
# Copyright (C) 2023 Cédric Krier
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

# This is a separate test file because it should not be run regularly
# because it could negatively impact the SEED service.

"""Extra tests for the stdnum.eu.excise module."""

import os
import unittest

from stdnum.eu import excise


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestSeed(unittest.TestCase):
    """Test the SEED web service provided by the European commission for
    validation Excise numbers of European countries."""

    def test_check_seed(self):
        """Test stdnum.eu.excise.check_seed()"""
        result = excise.check_seed('FR012907E0820')
        self.assertTrue('errorDescription' not in result)
        self.assertTrue(len(result['result']) > 0)
        first = result['result'][0]
        self.assertEqual(first['excise'], 'FR012907E0820')
