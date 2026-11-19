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
# License along with this library; if not, see <https://www.gnu.org/licenses/>.

# This is a separate test file because it should not be run regularly
# because it could negatively impact the VIES service.

"""Extra tests for the stdnum.eu.vat module."""

import os
import unittest
from unittest.mock import Mock, patch

from stdnum.eu import vat


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestVies(unittest.TestCase):
    """Test the VIES web service provided by the European commission for
    validation VAT numbers of European countries."""

    def test_check_vies(self) -> None:
        """Test stdnum.eu.vat.check_vies()"""
        result = vat.check_vies('NL4495445B01')
        self.assertTrue(result['valid'])
        self.assertEqual(result['countryCode'], 'NL')
        self.assertEqual(result['vatNumber'], '004495445B01')

    def test_check_vies_approx(self) -> None:
        """Test stdnum.eu.vat.check_vies_approx()"""
        result = vat.check_vies_approx('NL4495445B01', 'NL4495445B01')
        self.assertTrue(result['valid'])
        self.assertEqual(result['countryCode'], 'NL')
        self.assertEqual(result['vatNumber'], '004495445B01')


class TestViesRestOptions(unittest.TestCase):
    """Test the REST request options without contacting the VIES service."""

    def test_check_vies_request_options(self) -> None:
        """Forward timeout and CA configuration to the REST client."""
        requests = Mock()
        requests.post.return_value.json.return_value = {'valid': True}
        with patch.dict('sys.modules', {'requests': requests}):
            result = vat.check_vies('BE0428759497', timeout=2.5, verify='/tmp/ca.pem')
        self.assertTrue(result['valid'])
        requests.post.assert_called_once_with(
            'https://ec.europa.eu/taxation_customs/vies/rest-api/check-vat-number',
            json={'countryCode': 'BE', 'vatNumber': '0428759497'},
            timeout=2.5, verify='/tmp/ca.pem')

    def test_check_vies_approx_request_options(self) -> None:
        """Forward timeout and TLS settings for approximate lookups."""
        requests = Mock()
        requests.post.return_value.json.return_value = {'valid': True}
        with patch.dict('sys.modules', {'requests': requests}):
            result = vat.check_vies_approx('BE0428759497', 'BE0428759497', timeout=7, verify=False)
        self.assertTrue(result['valid'])
        requests.post.assert_called_once_with(
            'https://ec.europa.eu/taxation_customs/vies/rest-api/check-vat-number',
            json={
                'countryCode': 'BE',
                'vatNumber': '0428759497',
                'requesterCountryCode': 'BE',
                'requesterVatNumber': '0428759497',
            },
            timeout=7, verify=False)
