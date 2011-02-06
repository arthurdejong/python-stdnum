# __init__.py - main module
# coding: utf-8
#
# Copyright (C) 2010, 2011 Arthur de Jong
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

"""A Python module to parse, validate and reformat standard numbers
and codes in different formats.

Currently this module supports the following formats:

 * ISBN (International Standard Book Number)
 * ISSN (International Standard Serial Number)
 * ISMN (International Standard Music Number)
 * ISAN (International Standard Audiovisual Number)
 * BSN (Burgerservicenummer, the Dutch national identification number)
 * CPF (Cadastro de Pessoas Físicas, the Brazillian national identification
   number)
 * SSN (U.S. Social Security Number)
 * IMEI (International Mobile Equipment Identity)
 * MEID (Mobile Equipment Identifier)
 * GRid (Global Release Identifier)
 * IBAN (International Bank Account Number)
 * ISIL (International Standard Identifier for Libraries and Related
   Organizations)

Furthermore a number of generic check digit algorithms are available:

 * the Verhoeff algorithm
 * the Luhn and Luhn mod N algorithms
 * some algorithms described in ISO/IEC 7064: Mod 11, 2, Mod 37, 2,
   Mod 97, 10, Mod 11, 10 and Mod 37, 36
"""
