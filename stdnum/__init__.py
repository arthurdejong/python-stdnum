# __init__.py - main module
# coding: utf-8
#
# Copyright (C) 2010-2017 Arthur de Jong
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

* al.nipt: NIPT (Numri i Identifikimit për Personin e Tatueshëm, Albanian VAT number)
* ar.cbu: CBU (Clave Bancaria Uniforme, Argentine bank account number)
* ar.cuit: CUIT (Código Único de Identificación Tributaria, Argentinian tax number)
* at.businessid: Austrian Company Register Numbers
* at.uid: UID (Umsatzsteuer-Identifikationsnummer, Austrian VAT number)
* au.abn: ABN (Australian Business Number)
* au.acn: ACN (Australian Company Number)
* au.tfn: TFN (Australian Tax File Number)
* be.vat: BTW, TVA, NWSt, ondernemingsnummer (Belgian enterprise number)
* bg.egn: EGN (ЕГН, Единен граждански номер, Bulgarian personal identity codes)
* bg.pnf: PNF (ЛНЧ, Личен номер на чужденец, Bulgarian number of a foreigner)
* bg.vat: VAT (Идентификационен номер по ДДС, Bulgarian VAT number)
* br.cnpj: CNPJ (Cadastro Nacional da Pessoa Jurídica, Brazillian company identifier)
* br.cpf: CPF (Cadastro de Pessoas Físicas, Brazillian national identifier)
* ch.ssn: Swiss social security number ("Sozialversicherungsnummer")
* ch.uid: UID (Unternehmens-Identifikationsnummer, Swiss business identifier)
* ch.vat: VAT, MWST, TVA, IVA, TPV (Mehrwertsteuernummer, the Swiss VAT number)
* cl.rut: RUT (Rol Único Tributario, Chilean national tax number)
* cn.ric: RIC No. (Chinese Resident Identity Card Number)
* co.nit: NIT (Número De Identificación Tributaria, Colombian identity code)
* cusip: CUSIP number (financial security identification number)
* cy.vat: Αριθμός Εγγραφής Φ.Π.Α. (Cypriot VAT number)
* cz.dic: DIČ (Daňové identifikační číslo, Czech VAT number)
* cz.rc: RČ (Rodné číslo, the Czech birth number)
* de.vat: Ust ID Nr. (Umsatzsteur Identifikationnummer, German VAT number)
* de.wkn: Wertpapierkennnummer (German securities identification code)
* dk.cpr: CPR (personnummer, the Danish citizen number)
* dk.cvr: CVR (Momsregistreringsnummer, Danish VAT number)
* do.cedula: Cedula (Dominican Republic national identification number)
* do.rnc: RNC (Registro Nacional del Contribuyente, Dominican Republic tax number)
* ean: EAN (International Article Number)
* ec.ci: CI (Cédula de identidad, Ecuadorian personal identity code)
* ec.ruc: RUC (Registro Único de Contribuyentes, Ecuadorian company tax number)
* ee.ik: Isikukood (Estonian Personcal ID number)
* ee.kmkr: KMKR (Käibemaksukohuslase, Estonian VAT number)
* es.ccc: CCC (Código Cuenta Corriente, Spanish Bank Account Code)
* es.cif: CIF (Certificado de Identificación Fiscal, Spanish company tax number)
* es.cups: CUPS (Código Unificado de Punto de Suministro, Supply Point Unified Code)
* es.dni: DNI (Documento nacional de identidad, Spanish personal identity codes)
* es.iban: Spanish IBAN (International Bank Account Number)
* es.nie: NIE (Número de Identificación de Extranjeros, Spanish foreigner number)
* es.nif: NIF (Número de Identificación Fiscal, Spanish VAT number)
* es.referenciacatastral: Referencia Catastral (Spanish real estate property id)
* eu.at_02: SEPA Identifier of the Creditor (AT-02)
* eu.eic: EIC (European Energy Identification Code)
* eu.nace: NACE (classification for businesses in the European Union)
* eu.vat: VAT (European Union VAT number)
* fi.alv: ALV nro (Arvonlisäveronumero, Finnish VAT number)
* fi.associationid: Finnish Association Identifier
* fi.hetu: HETU (Henkilötunnus, Finnish personal identity code)
* fi.ytunnus: Y-tunnus (Finnish business identifier)
* fr.nif: NIF (Numéro d'Immatriculation Fiscale, French tax identification number)
* fr.nir: NIR (French personal identification number)
* fr.siren: SIREN (a French company identification number)
* fr.siret: SIRET (a French company establishment identification number)
* fr.tva: n° TVA (taxe sur la valeur ajoutée, French VAT number)
* gb.nhs: NHS (United Kingdom National Health Service patient identifier)
* gb.sedol: SEDOL number (Stock Exchange Daily Official List number)
* gb.vat: VAT (United Kingdom (and Isle of Man) VAT registration number)
* gr.vat: FPA, ΦΠΑ, ΑΦΜ (Αριθμός Φορολογικού Μητρώου, the Greek VAT number)
* grid: GRid (Global Release Identifier)
* hr.oib: OIB (Osobni identifikacijski broj, Croatian identification number)
* hu.anum: ANUM (Közösségi adószám, Hungarian VAT number)
* iban: IBAN (International Bank Account Number)
* ie.pps: PPS No (Personal Public Service Number, Irish personal number)
* ie.vat: VAT (Irish tax reference number)
* imei: IMEI (International Mobile Equipment Identity)
* imo: IMO number (International Maritime Organization number)
* imsi: IMSI (International Mobile Subscriber Identity)
* is_.kennitala: Kennitala (Icelandic personal and organisation identity code)
* is_.vsk: VSK number (Virðisaukaskattsnúmer, Icelandic VAT number)
* isan: ISAN (International Standard Audiovisual Number)
* isbn: ISBN (International Standard Book Number)
* isil: ISIL (International Standard Identifier for Libraries)
* isl.vsk: VSK (Virðisaukaskattsnúmer, Icelandic VAT number)
* isl.kennitala: Kennitala (Icelandic personal and organisation identity number)
* ismn: ISMN (International Standard Music Number)
* iso6346: ISO 6346 (International standard for container identification)
* iso9362: ISO 9362 (Business identifier codes)
* issn: ISSN (International Standard Serial Number)
* it.codicefiscale: Codice Fiscale (Italian tax code for individuals)
* it.iva: Partita IVA (Italian VAT number)
* lei: LEI (Legal Entity Identifier)
* lt.pvm: PVM (Pridėtinės vertės mokestis mokėtojo kodas, Lithuanian VAT number)
* lu.tva: TVA (taxe sur la valeur ajoutée, Luxembourgian VAT number)
* lv.pvn: PVN (Pievienotās vērtības nodokļa, Latvian VAT number)
* mc.tva: n° TVA (taxe sur la valeur ajoutée, Monacan VAT number)
* meid: MEID (Mobile Equipment Identifier)
* mt.vat: VAT (Maltese VAT number)
* mx.rfc: RFC (Registro Federal de Contribuyentes, Mexican tax number)
* my.nric: NRIC No. (Malaysian National Registration Identity Card Number)
* nl.brin: Brin number (Dutch number for schools)
* nl.bsn: BSN (Burgerservicenummer, Dutch national identification number)
* nl.btw: BTW-nummer (Omzetbelastingnummer, the Dutch VAT number)
* nl.onderwijsnummer: Onderwijsnummer (Dutch student school number)
* nl.postcode: Postcode (Dutch postal code)
* no.mva: MVA (Merverdiavgift, Norwegian VAT number)
* no.orgnr: Orgnr (Organisasjonsnummer, Norwegian organization number)
* pl.nip: NIP (Numer Identyfikacji Podatkowej, Polish VAT number)
* pl.pesel: PESEL (Polish national identification number)
* pl.regon: REGON (Rejestr Gospodarki Narodowej, Polish register of economic units)
* pt.nif: NIF (Número de identificação fiscal, Portuguese VAT number)
* ro.cf: CF (Cod de înregistrare în scopuri de TVA, Romanian VAT number)
* ro.cnp: CNP (Cod Numeric Personal, Romanian Numerical Personal Code)
* rs.pib: PIB (Poreski Identifikacioni Broj, Serbian tax identification number)
* ru.inn: ИНН (Идентификационный номер налогоплательщика, Russian tax identifier)
* se.orgnr: Orgnr (Organisationsnummer, Swedish company number)
* se.vat: VAT (Moms, Mervärdesskatt, Swedish VAT number)
* si.ddv: ID za DDV (Davčna številka, Slovenian VAT number)
* sk.dph: IČ DPH (IČ pre daň z pridanej hodnoty, Slovak VAT number)
* sk.rc: RČ (Rodné číslo, the Slovak birth number)
* sm.coe: COE (Codice operatore economico, San Marino national tax number)
* tr.tckimlik: T.C. Kimlik No. (Turkish personal identification number)
* us.atin: ATIN (U.S. Adoption Taxpayer Identification Number)
* us.ein: EIN (U.S. Employer Identification Number)
* us.itin: ITIN (U.S. Individual Taxpayer Identification Number)
* us.ptin: PTIN (U.S. Preparer Tax Identification Number)
* us.rtn: RTN (Routing transport number)
* us.ssn: SSN (U.S. Social Security Number)
* us.tin: TIN (U.S. Taxpayer Identification Number)

Furthermore a number of generic check digit algorithms are available:

* damm: The Damm algorithm
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

Apart from the validate() function, many modules provide extra
parsing, validation, formatting or conversion functions.
"""


# the version number of the library
__version__ = '1.6'
