# __init__.py - main module
# coding: utf-8
#
# Copyright (C) 2010-2014 Arthur de Jong
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

"""Parse, validate and reformat standard numbers and codes.

This library offers functions for parsing, validating and reformatting
standard numbers and codes in various formats.

Currently this package supports the following formats:

* at.uid: UID (Umsatzsteuer-Identifikationsnummer, Austrian VAT number)
* be.vat: BTW, TVA, NWSt (Belgian VAT number)
* bg.egn: EGN (ЕГН, Единен граждански номер, Bulgarian personal identity codes)
* bg.pnf: PNF (ЛНЧ, Личен номер на чужденец, Bulgarian number of a foreigner)
* bg.vat: VAT (Идентификационен номер по ДДС, Bulgarian VAT number)
* br.cpf: CPF (Cadastro de Pessoas Físicas, Brazillian national identifier)
* ch.ssn: Swiss social security number ("Sozialversicherungsnummer")
* cn.ric: RIC No. (Chinese Resident Identity Card Number)
* cy.vat: Αριθμός Εγγραφής Φ.Π.Α. (Cypriot VAT number)
* cz.dic: DIČ (Daňové identifikační číslo, Czech VAT number)
* cz.rc: RČ (Rodné číslo, the Czech birth number)
* de.vat: Ust ID Nr. (Umsatzsteur Identifikationnummer, German VAT number)
* dk.cpr: CPR (personnummer, the Danish citizen number)
* dk.cvr: CVR (Momsregistreringsnummer, Danish VAT number)
* ean: EAN (International Article Number)
* ec.ci: CI (Cédula de identidad, Ecuadorian personal identity code)
* ec.ruc: RUC (Registro Único de Contribuyentes, Ecuadorian company tax number)
* ee.kmkr: KMKR (Käibemaksukohuslase, Estonian VAT number)
* es.cif: CIF (Certificado de Identificación Fiscal, Spanish company tax number)
* es.dni: DNI (Documento nacional de identidad, Spanish personal identity codes)
* es.nie: NIE (Número de Identificación de Extranjeros, Spanish foreigner number)
* es.nif: NIF (Número de Identificación Fiscal, Spanish VAT number)
* eu.at_02: SEPA Identifier of the Creditor (AT-02)
* eu.vat: VAT (European Union VAT number)
* fi.alv: ALV nro (Arvonlisäveronumero, Finnish VAT number)
* fi.hetu: HETU (Henkilötunnus, Finnish personal identity code)
* fr.siren: SIREN (a French company identification number)
* fr.tva: n° TVA (taxe sur la valeur ajoutée, French VAT number)
* gb.vat: VAT (United Kingdom (and Isle of Man) VAT registration number)
* gr.vat: FPA, ΦΠΑ (Foros Prostithemenis Aksias, the Greek VAT number)
* grid: GRid (Global Release Identifier)
* hr.oib: OIB (Osobni identifikacijski broj, Croatian identification number)
* hu.anum: ANUM (Közösségi adószám, Hungarian VAT number)
* iban: IBAN (International Bank Account Number)
* ie.pps: PPS No (Personal Public Service Number, Irish personal number)
* ie.vat: VAT (Irish VAT number)
* imei: IMEI (International Mobile Equipment Identity)
* imsi: IMSI (International Mobile Subscriber Identity)
* isan: ISAN (International Standard Audiovisual Number)
* isbn: ISBN (International Standard Book Number)
* isil: ISIL (International Standard Identifier for Libraries)
* ismn: ISMN (International Standard Music Number)
* iso6346: ISO 6346 (International standard for container identification)
* issn: ISSN (International Standard Serial Number)
* it.codicefiscale: Codice Fiscale (Italian tax code for individuals)
* it.iva: Partita IVA (Italian VAT number)
* lt.pvm: PVM (Pridėtinės vertės mokestis mokėtojo kodas, Lithuanian VAT number)
* lu.tva: TVA (taxe sur la valeur ajoutée, Luxembourgian VAT number)
* lv.pvn: PVN (Pievienotās vērtības nodokļa, Latvian VAT number)
* meid: MEID (Mobile Equipment Identifier)
* mt.vat: VAT (Maltese VAT number)
* my.nric: NRIC No. (Malaysian National Registration Identity Card Number)
* nl.brin: Brin number (Dutch number for schools)
* nl.bsn: BSN (Burgerservicenummer, Dutch national identification number)
* nl.btw: BTW-nummer (Omzetbelastingnummer, the Dutch VAT number)
* nl.onderwijsnummer: Onderwijsnummer (Dutch student school number)
* nl.postcode: Postcode (Dutch postal code)
* pl.nip: NIP (Numer Identyfikacji Podatkowej, Polish VAT number)
* pt.nif: NIF (Número de identificação fiscal, Portuguese VAT number)
* ro.cf: CF (Cod de înregistrare în scopuri de TVA, Romanian VAT number)
* ro.cnp: CNP (Cod Numeric Personal, Romanian Numerical Personal Code)
* se.vat: VAT (Moms, Mervärdesskatt, Swedish VAT number)
* si.ddv: ID za DDV (Davčna številka, Slovenian VAT number)
* sk.dph: IČ DPH (IČ pre daň z pridanej hodnoty, Slovak VAT number)
* sk.rc: RČ (Rodné číslo, the Slovak birth number)
* us.atin: ATIN (U.S. Adoption Taxpayer Identification Number)
* us.ein: EIN (U.S. Employer Identification Number)
* us.itin: ITIN (U.S. Individual Taxpayer Identification Number)
* us.ptin: PTIN (U.S. Preparer Tax Identification Number)
* us.rtn: RTN (Routing transport number)
* us.ssn: SSN (U.S. Social Security Number)
* us.tin: TIN (U.S. Taxpayer Identification Number)

Furthermore a number of generic check digit algorithms are available:

* iso7064.mod_11_10: The ISO 7064 Mod 11, 10 algorithm
* iso7064.mod_11_2: The ISO 7064 Mod 11, 2 algorithm
* iso7064.mod_37_2: The ISO 7064 Mod 37, 2 algorithm
* iso7064.mod_37_36: The ISO 7064 Mod 37, 36 algorithm
* iso7064.mod_97_10: The ISO 7064 Mod 97, 10 algorithm
* luhn: The Luhn and Luhn mod N algorithms
* verhoeff: The Verhoeff algorithm

All modules implement a common interface:

>>> from stdnum import isbn
>>> isbn.validate('978-9024538270')
'9789024538270'
>>> isbn.validate('978-9024538271')
Traceback (most recent call last):
    ...
InvalidChecksum: ...

Apart from the validate() function, modules generally provide extra
parsing, validation, formatting or conversion functions.
"""


# the version number of the library
__version__ = '1.0'
