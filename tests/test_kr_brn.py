# test_kr_brn.py - functions for testing the online BRN validation
# coding: utf-8
#
# Copyright (C) 2020 Arthur de Jong
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

"""Extra tests for the stdnum.kr.brn module."""

import os
import unittest

from stdnum.kr import brn


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestFTC(unittest.TestCase):
    """Test the check provided based on the Korea Fair Trade Commission
    website."""

    def test_check_ftc(self):
        """Test stdnum.kr.brn.check_ftc()"""
        # Test a normal valid number
        result = brn.check_ftc('109-81-39795')
        self.assertTrue(result)
        # Test an invalid number
        result = brn.check_ftc('109-81-39796')
        self.assertIsNone(result)
