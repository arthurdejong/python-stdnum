# test_do_cedula.py - functions for testing the online Cedula validation
# coding: utf-8
#
# Copyright (C) 2018 Arthur de Jong
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

"""Extra tests for the stdnum.do.cedula module."""

import os
import unittest

from stdnum.do import cedula


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestDGII(unittest.TestCase):
    """Test the web services provided by the the Dirección General de
    Impuestos Internos (DGII), the Dominican Republic tax department."""

    def test_check_dgii(self):
        """Test stdnum.do.cedula.check_dgii()"""
        # Test a normal valid number
        result = cedula.check_dgii('05500023407')
        self.assertTrue(all(
            key in result.keys()
            for key in ['cedula', 'name', 'commercial_name', 'category', 'status']))
        self.assertEqual(result['cedula'], '05500023407')
        # Test an invalid length number
        self.assertIsNone(cedula.check_dgii('123'))
        # Test a number with an invalid checksum
        self.assertIsNone(cedula.check_dgii('00113918204'))
        # Valid number but unknown
        self.assertIsNone(cedula.check_dgii('12345678903'))
        # Test a number on the whitelist
        result = cedula.check_dgii('02300052220')
        self.assertEqual(result['cedula'], '02300052220')
