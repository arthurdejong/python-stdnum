# test_eu_vat.py - functions for testing the UID Webservice
# coding: utf-8
#
# Copyright (C) 2022 Arthur de Jong
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

"""Extra tests for the stdnum.ch.uid module."""

import os
import unittest

from stdnum.ch import uid


@unittest.skipIf(
    not os.environ.get('ONLINE_TESTS'),
    'Do not overload online services')
class TestUid(unittest.TestCase):
    """Test the UID Webservice provided by the Swiss Federal Statistical
    Office for validating UID numbers."""

    def test_check_uid(self):
        """Test stdnum.ch.uid.check_uid()"""
        result = uid.check_uid('CHE113690319')
        self.assertTrue(result)
        self.assertEqual(result['organisation']['organisationIdentification']['uid']['uidOrganisationId'], 113690319)
        self.assertEqual(result['organisation']['organisationIdentification']['legalForm'], '0220')
        self.assertEqual(result['vatRegisterInformation']['vatStatus'], '2')
