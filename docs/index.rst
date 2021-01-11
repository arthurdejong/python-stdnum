.. module:: stdnum

.. include:: ../README
   :end-before: Available formats


Common Interface
----------------

Most of the number format modules implement the following functions:

.. function:: module.validate(number)

   Validate the number and return a compact, consistent representation of
   the number or code. If the validation fails,
   :mod:`an exception <.exceptions>` is raised that indicates the type of
   error.

   :raises ValidationError: When the specified number is invalid
   :returns:  str -- A compact (canonical) representation of the number

.. function:: module.is_valid(number)

   Return either ``True`` or ``False`` depending on whether the passed number
   is in any supported and valid form and passes all embedded checks of the
   number. This function should never raise an exception.

   :returns: bool -- ``True`` if validated, ``False`` otherwise

.. function:: module.compact(number)

   Return a compact representation of the number or code. This function
   generally does not do validation but may raise exceptions for wildly
   invalid numbers.

   :returns: str -- The compacted number

.. function:: module.format(number)

   Return a formatted version of the number in the preferred format.
   This function generally expects to be passed a valid number or code and
   may raise exceptions for invalid numbers.

   :returns: str -- A formatted number

The check digit modules generally also provide the following functions:

.. function:: module.checksum(number)

   Calculate the checksum over the provided number. This is generally a
   number that can be used to determine whether the provided number is
   valid. It depends on the algorithm which checksum is considered valid.

   :returns: int -- A numeric checksum over the number

.. function:: module.calc_check_digit(number)

   Calculate the check digit that should be added to the number to make it
   valid.

   :returns: str -- A check digit that can be appended

Apart from the above, the modules may add extra parsing, validation or
conversion functions.


Helper functions and modules
----------------------------

.. autosummary::
   :toctree:

   exceptions

.. autofunction:: get_cc_module

   Searches the stdnum collection of modules for a number format for a
   particular country. `name` may be an aliased name. For example:

       >>> from stdnum import get_cc_module
       >>> mod = get_cc_module('nl', 'vat')
       >>> mod
       <module 'stdnum.nl.btw' from '...'>
       >>> mod.validate('004495445B01')
       '004495445B01'

   Will return ``None`` if no module could be found. The generic names that
   are currently in use:

   * ``'vat'`` for value added tax numbers
   * ``'businessid'`` for generic business identifiers (although some countries
     may have multiple)
   * ``'personalid'`` for generic personal identifiers (some countries may have
     multiple, especially for tax purposes)
   * ``'postcal_code'`` for address postal codes


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

   ad.nrt
   al.nipt
   ar.cbu
   ar.cuit
   ar.dni
   at.businessid
   at.postleitzahl
   at.tin
   at.uid
   at.vnr
   au.abn
   au.acn
   au.tfn
   be.iban
   be.vat
   bg.egn
   bg.pnf
   bg.vat
   bic
   bitcoin
   br.cnpj
   br.cpf
   by.unp
   ca.bn
   ca.sin
   casrn
   ch.esr
   ch.ssn
   ch.uid
   ch.vat
   cl.rut
   cn.ric
   cn.uscc
   co.nit
   cr.cpf
   cr.cpj
   cr.cr
   cu.ni
   cusip
   cy.vat
   cz.dic
   cz.rc
   de.handelsregisternummer
   de.idnr
   de.stnr
   de.vat
   de.wkn
   dk.cpr
   dk.cvr
   do.cedula
   do.ncf
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
   eu.banknote
   eu.eic
   eu.nace
   eu.vat
   fi.alv
   fi.associationid
   fi.hetu
   fi.veronumero
   fi.ytunnus
   figi
   fr.nif
   fr.nir
   fr.siren
   fr.siret
   fr.tva
   gb.nhs
   gb.sedol
   gb.upn
   gb.utr
   gb.vat
   gr.amka
   gr.vat
   grid
   gs1_128
   gt.nit
   hr.oib
   hu.anum
   iban
   id.npwp
   ie.pps
   ie.vat
   il.hp
   il.idnr
   imei
   imo
   imsi
   in_.aadhaar
   in_.pan
   is_.kennitala
   is_.vsk
   isan
   isbn
   isil
   isin
   ismn
   iso11649
   iso6346
   issn
   it.aic
   it.codicefiscale
   it.iva
   jp.cn
   kr.brn
   kr.rrn
   lei
   li.peid
   lt.asmens
   lt.pvm
   lu.tva
   lv.pvn
   mac
   mc.tva
   md.idno
   me.iban
   meid
   mt.vat
   mu.nid
   mx.curp
   mx.rfc
   my.nric
   nl.brin
   nl.bsn
   nl.btw
   nl.onderwijsnummer
   nl.postcode
   no.fodselsnummer
   no.iban
   no.kontonr
   no.mva
   no.orgnr
   nz.bankaccount
   nz.ird
   pe.cui
   pe.ruc
   pl.nip
   pl.pesel
   pl.regon
   pt.nif
   py.ruc
   ro.cf
   ro.cnp
   ro.cui
   ro.onrc
   rs.pib
   ru.inn
   se.orgnr
   se.personnummer
   se.vat
   sg.uen
   si.ddv
   sk.dph
   sk.rc
   sm.coe
   sv.nit
   tr.tckimlik
   tr.vkn
   tw.ubn
   ua.edrpou
   ua.rntrc
   us.atin
   us.ein
   us.itin
   us.ptin
   us.rtn
   us.ssn
   us.tin
   uy.rut
   vatin
   ve.rif
   vn.mst
   za.idnr
   za.tin


Changes in python-stdnum
------------------------

.. toctree::
   :maxdepth: 2

   changes
