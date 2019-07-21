# test_de_handelsregisternummer.py - online validation tests
# coding: utf-8
#
# Copyright (C) 2019 Arthur de Jong
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

"""Extra tests for the stdnum.de.handelsregisternummer module."""

import os
import unittest

from stdnum.de import handelsregisternummer


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestOffeneRegister(unittest.TestCase):
    """Test the web services provided by the OffeneRegister.de web site."""

    def test_check_offeneregister(self):
        """Test stdnum.de.handelsregisternummer.check_offeneregister()"""
        # Test a normal valid number
        result = handelsregisternummer.check_offeneregister('Chemnitz HRB 14011')
        self.assertTrue(all(
            key in result.keys()
            for key in ['company_number', 'current_status', 'federal_state', 'registrar', 'native_company_number']))
        # Test invalid number
        result = handelsregisternummer.check_offeneregister('Chemnitz HRA 14012')
        self.assertIsNone(result)
