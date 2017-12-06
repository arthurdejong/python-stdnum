.. module:: stdnum

.. include:: ../README
   :end-before: Available formats


Common Interface
----------------

Most of the number format modules implement the following functions:

.. function:: validate(number)

   Validate the number and return a compact, consistent representation of
   the number or code. If the validation fails,
   :mod:`an exception <.exceptions>` is raised that indicates the type of
   error.

.. function:: is_valid(number)

   Return either ``True`` or ``False`` depending on whether the passed number
   is in any supported and valid form and passes all embedded checks of the
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

   damm
   iso7064
   luhn
   verhoeff


Available formats
-----------------

.. autosummary::
   :toctree:

   al.nipt
   ar.cbu
   ar.cuit
   at.businessid
   at.uid
   au.abn
   au.acn
   au.tfn
   be.vat
   bg.egn
   bg.pnf
   bg.vat
   bic
   br.cnpj
   br.cpf
   ca.bn
   ca.sin
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
   de.idnr
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
   ee.registrikood
   es.ccc
   es.cif
   es.cups
   es.dni
   es.iban
   es.nie
   es.nif
   es.referenciacatastral
   eu.at_02
   eu.eic
   eu.nace
   eu.vat
   fi.alv
   fi.associationid
   fi.hetu
   fi.veronumero
   fi.ytunnus
   fr.nif
   fr.nir
   fr.siren
   fr.siret
   fr.tva
   gb.nhs
   gb.sedol
   gb.upn
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
   issn
   it.codicefiscale
   it.iva
   lei
   lt.pvm
   lu.tva
   lv.pvn
   mc.tva
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
   rs.pib
   ru.inn
   se.orgnr
   se.vat
   si.ddv
   sk.dph
   sk.rc
   sm.coe
   tr.tckimlik
   us.atin
   us.ein
   us.itin
   us.ptin
   us.rtn
   us.ssn
   us.tin
