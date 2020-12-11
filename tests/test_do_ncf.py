# test_do_ncf.py - functions for testing the online NCF validation
# coding: utf-8
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

# This is a separate test file because it should not be run regularly
# because it could negatively impact the online service.

"""Extra tests for the stdnum.do.ncf module."""

import os
import unittest

from stdnum.do import ncf


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestDGII(unittest.TestCase):
    """Test the web services provided by the the Dirección General de
    Impuestos Internos (DGII), the Dominican Republic tax department."""

    def test_check_dgii(self):
        """Test stdnum.do.ncf.check_dgii()"""
        # Test a normal valid number
        result = ncf.check_dgii('130546312', 'A010010011500000038')
        self.assertTrue(result)
        self.assertIn('name', result.keys())
        self.assertIn('rnc', result.keys())
        self.assertIn('ncf', result.keys())
        self.assertIn('validation_message', result.keys())
        self.assertEqual(result['rnc'], '130546312')
        self.assertEqual(result['ncf'], 'A010010011500000038')
        # Test an invalid combination
        self.assertIsNone(ncf.check_dgii('501620371', 'A010010011500000038'))
        # Another valid example
        self.assertTrue(ncf.check_dgii('1-31-56633-2', 'A010010010100000001'))
        self.assertTrue(ncf.check_dgii('1-31-56633-2', 'A010010010100000100'))
        # These types have not been requested with the regulator
        self.assertFalse(ncf.check_dgii('1-31-56633-2', 'A030010010100000001'))
        self.assertFalse(ncf.check_dgii('1-31-56633-2', 'A010020010100000001'))
        # Test the new format
        result = ncf.check_dgii('130546312', 'B0100000005')
        self.assertTrue(result)
        self.assertIn('name', result.keys())
        self.assertIn('rnc', result.keys())
        self.assertIn('ncf', result.keys())
        self.assertIn('validation_message', result.keys())
        self.assertEqual(result['rnc'], '130546312')
        self.assertEqual(result['ncf'], 'B0100000005')
        # Test the ENCF
        result = ncf.check_dgii('101010632', 'E310049533639',
                                buyer_rnc='22400559690', security_code='hnI63Q')
        self.assertTrue(result)
        self.assertIn('status', result.keys())
        self.assertEqual(result['issuing_rnc'], '101010632')
        self.assertEqual(result['buyer_rnc'], '22400559690')
        self.assertEqual(result['ncf'], 'E310049533639')
        self.assertIn('issuing_date', result.keys())
        self.assertIn('signature_date', result.keys())
        self.assertIn('total', result.keys())
        self.assertIn('total_itbis', result.keys())
        self.assertIn('validation_message', result.keys())
