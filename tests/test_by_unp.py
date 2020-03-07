# test_by_unp.py - online validation tests
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

"""Extra tests for the stdnum.by.unp module."""

import os
import unittest

from stdnum.by import unp


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestNalog(unittest.TestCase):
    """Test the web services provided by the portal.nalog.gov.by web site."""

    def test_check_nalog(self):
        """Test stdnum.by.unp.check_nalog()"""
        # Test a normal valid number
        result = unp.check_nalog('191682495')
        self.assertDictEqual(
            result,
            {
                'CKODSOST': '1',
                'DLIKV': None,
                'DREG': '08.07.2011',
                'NMNS': '104',
                'VKODS': 'Действующий',
                'VLIKV': None,
                'VMNS': 'Инспекция МНС по Московскому району г.Минска ',
                'VNAIMK': 'Частное предприятие "КРИОС ГРУПП"',
                'VNAIMP': 'Частное производственное унитарное предприятие "КРИОС ГРУПП"',
                'VPADRES': 'г. Минск,ул. Уманская, д.54, пом. 152',
                'VUNP': '191682495',
            })
        # Check that result has at least these keys
        keys = ['VUNP', 'VNAIMP', 'VNAIMK', 'DREG', 'CKODSOST', 'VKODS']
        self.assertEqual([key for key in keys if key in result], keys)
        self.assertEqual(result['VUNP'], '191682495')
        # Test invalid number
        result = unp.check_nalog('771681495')
        self.assertIsNone(result)
