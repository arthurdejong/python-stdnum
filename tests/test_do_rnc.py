# test_do_rnc.py - functions for testing the online RNC validation
# coding: utf-8
#
# Copyright (C) 2017-2023 Arthur de Jong
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
# because it could negatively impact the online service.

"""Extra tests for the stdnum.do.rnc module."""

import os
import unittest

from stdnum.do import rnc


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestDGII(unittest.TestCase):
    """Test the web services provided by the the Dirección General de
    Impuestos Internos (DGII), the Dominican Republic tax department."""

    def setUp(self):
        """Prepare the test."""
        # For Python 2.7 compatibility
        if not hasattr(self, 'assertRegex'):
            self.assertRegex = self.assertRegexpMatches

    def test_check_dgii(self):
        """Test stdnum.do.rnc.check_dgii()"""
        # Test a normal valid number
        result = rnc.check_dgii('131098193')
        self.assertTrue(all(
            key in result.keys()
            for key in ['rnc', 'name', 'commercial_name', 'category', 'status']))
        self.assertEqual(result['rnc'], '131098193')
        # Test an invalid length number
        self.assertIsNone(rnc.check_dgii('123'))
        # Test a number with an invalid checksum
        self.assertIsNone(rnc.check_dgii('112031226'))
        # Valid number but unknown
        self.assertIsNone(rnc.check_dgii('814387152'))
        # Test a number on the whitelist
        result = rnc.check_dgii('501658167')
        self.assertEqual(result['rnc'], '501658167')
        # Test the output unescaping (\t and \n) of the result so JSON
        # deserialisation works
        result = rnc.check_dgii('132070801')
        self.assertEqual(result['rnc'], '132070801')

    def test_search_dgii(self):
        """Test stdnum.do.rnc.search_dgii()"""
        # Search for some existing companies
        results = rnc.search_dgii('EXPORT DE')
        self.assertGreaterEqual(len(results), 3)
        self.assertRegex(results[0]['rnc'], r'\d{9}')
        self.assertRegex(results[1]['rnc'], r'\d{9}')
        self.assertRegex(results[2]['rnc'], r'\d{9}')
        # Check maximum rows parameter
        two_results = rnc.search_dgii('EXPORT DE', end_at=2)
        self.assertEqual(len(two_results), 2)
        self.assertEqual(two_results, results[:2])
        # Check the start_at parameter
        two_results = rnc.search_dgii('EXPORT DE', end_at=3, start_at=2)
        self.assertEqual(len(two_results), 2)
        self.assertEqual(two_results, results[1:3])
        # Check non-existing company
        results = rnc.search_dgii('NON-EXISTING COMPANY')
        self.assertEqual(results, [])
