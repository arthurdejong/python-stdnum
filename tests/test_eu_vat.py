# test_eu_vat.py - functions for testing the online VIES VAT validation
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
# because it could negatively impact the VIES service.

"""Extra tests for the stdnum.eu.vat module."""

import os
import unittest

from stdnum.eu import vat


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestVies(unittest.TestCase):
    """Test the VIES web service provided by the European commission for
    validation VAT numbers of European countries."""

    def test_check_vies(self):
        """Test stdnum.eu.vat.check_vies()"""
        result = vat.check_vies('BE555445')
        self.assertEqual(result['countryCode'], 'BE')
        self.assertEqual(result['vatNumber'], '555445')

    def test_check_vies_approx(self):
        """Test stdnum.eu.vat.check_vies_approx()"""
        result = vat.check_vies_approx('BE555445', 'BE555445')
        self.assertEqual(result['countryCode'], 'BE')
        self.assertEqual(result['vatNumber'], '555445')
