.. module:: stdnum

python-stdnum
=============

A Python module to parse, validate and reformat standard numbers and codes
in different formats. It contains a large collection of number formats.

Basically any number or code that has some validation mechanism available
or some common formatting is eligible for inclusion in this library.

http://arthurdejong.org/python-stdnum/


Common Interface
----------------

Most of the number format modules implement the following functions:

.. function:: validate(number)

   Validate the number and return a compact, consistent representation of
   the number or code. If the validation fails,
   :mod:`an exception <.exceptions>` is raised that indicates the type of
   error.

.. function:: is_valid(number)

   Return either True or False depending on whether the passed number is
   in any supported and valid form and passes all embedded checks of the
   number. This function should never raise an exception.

.. function:: compact(number)

   Return a compact representation of the number or code. This function
   generally does not do validation but may raise exceptions for wildly
   invalid numbers.

.. function:: format(number)

   Return a formatted version of the number in the preferred format.
   This function generally expects to be passed a valid number or code and
   may raise exceptions for invalid numbers.

The check digit modules generally also provide the following functions:

.. function:: checksum(number)

   Calculate the checksum over the provided number. This is generally a
   number that can be used to determine whether the provided number is
   valid. It depends on the algorithm which checksum is considered valid.

.. function:: calc_check_digit(number)

   Calculate the check digit that should be added to the number to make it
   valid.

Apart from the above, the modules may add extra parsing, validation or
conversion functions.


Helper modules
--------------

.. autosummary::
   :toctree:

   exceptions


Generic check digit algorithms
------------------------------

.. autosummary::
   :toctree:

   iso7064
   luhn
   verhoeff


Available formats
-----------------

.. autosummary::
   :toctree:

   al.nipt
   ar.cuit
   at.businessid
   at.uid
   be.vat
   bg.egn
   bg.pnf
   bg.vat
   br.cnpj
   br.cpf
   ch.ssn
   ch.uid
   ch.vat
   cl.rut
   cn.ric
   co.nit
   cusip
   cy.vat
   cz.dic
   cz.rc
   de.vat
   de.wkn
   dk.cpr
   dk.cvr
   do.cedula
   do.rnc
   ean
   ec.ci
   ec.ruc
   ee.ik
   ee.kmkr
   es.cif
   es.dni
   es.nie
   es.nif
   eu.at_02
   eu.vat
   fi.alv
   fi.associationid
   fi.hetu
   fi.ytunnus
   fr.siren
   fr.siret
   fr.tva
   gb.sedol
   gb.vat
   gr.vat
   grid
   hr.oib
   hu.anum
   iban
   ie.pps
   ie.vat
   imei
   imo
   imsi
   is_.kennitala
   is_.vsk
   isan
   isbn
   isil
   isin
   ismn
   iso6346
   iso9362
   issn
   it.codicefiscale
   it.iva
   lt.pvm
   lu.tva
   lv.pvn
   meid
   mt.vat
   mx.rfc
   my.nric
   nl.brin
   nl.bsn
   nl.btw
   nl.onderwijsnummer
   nl.postcode
   no.mva
   no.orgnr
   pl.nip
   pl.pesel
   pl.regon
   pt.nif
   ro.cf
   ro.cnp
   ru.inn
   se.orgnr
   se.vat
   si.ddv
   sk.dph
   sk.rc
   sm.coe
   us.atin
   us.ein
   us.itin
   us.ptin
   us.rtn
   us.ssn
   us.tin
