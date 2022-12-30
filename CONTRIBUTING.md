Contributing to python-stdnum
=============================

This document describes general guidelines for contributing new formats or
other enhancement to python-stdnum.


Adding number formats
---------------------

Basically any number or code that has some validation mechanism available or
some common formatting is eligible for inclusion into this library. If the
only specification of the number is "it consists of 6 digits" implementing
validation may not be that useful.

Contributions of new formats or requests to implement validation for a format
should include the following:

* The format name and short description.
* References to (official) sources that describe the format.
* A one or two paragraph description containing more details of the number
  (e.g. purpose and issuer and possibly format information that might be
  useful to end users).
* If available, a link to an (official) validation service for the number,
  reference implementations or similar sources that allow validating the
  correctness of the implementation.
* A set of around 20 to 100 "real" valid numbers for testing (more is better
  during development but only around 100 will be retained for regression
  testing).
* If the validation depends on some (online) list of formats, structures or
  parts of the identifier (e.g. a list of region codes that are part of the
  number) a way to easily update the registry information should be
  available.


Code contributions
------------------

Improvements to python-stdnum are most welcome. Integrating contributions
will be done on a best-effort basis and can be made easier if the following
are considered:

* Ideally contributions are made as GitHub pull requests, but contributions
  by email (privately or through the python-stdnum-users mailing list) can
  also be considered.
* Submitted contributions will often be reformatted and sometimes
  restructured for consistency with other parts.
* Contributions will be acknowledged in the release notes.
* Contributions should add or update a copyright statement if you feel the
  contribution is significant.
* All contribution should be made with compatible applicable copyright.
* It is not needed to modify the NEWS, README.md or files under docs for new
  formats; these files will be updated on release.
* Marking valid numbers as invalid should be avoided and are much worse than
  marking invalid numbers as valid. Since the primary use case for
  python-stdnum is to validate entered data having an implementation that
  results in "computer says no" should be avoided.
* Number format implementations should include links to sources of
  information: generally useful links (e.g. more details about the number
  itself) should be in the module docstring, if it relates more to the
  implementation (e.g. pointer to reference implementation, online API
  documentation or similar) a comment in the code is better
* Country-specific numbers and codes go in a country or region package (e.g.
  stdnum.eu.vat or stdnum.nl.bsn) while global numbers go in the toplevel
  name space (e.g. stdnum.isbn).
* All code should be well tested and achieve 100% code coverage.
* Existing code structure conventions (e.g. see README for interface) should
  be followed.
* Git commit messages should follow the usual 7 rules.
* Declarative or functional constructs are preferred over an iterative
  approach, e.g.::

      s = sum(int(c) for c in number)

  over::

      s = 0
      for c in number:
          s += int(c)


Testing
-------

Tests can be run with `tox`. Some basic code style tests can be run with `tox
-e flake8` and most other targets run the test suite with various supported
Python interpreters.

Module implementations have a couple of smaller test cases that also serve as
basic documentation of the happy flow.

More extensive tests are available, per module, in the tests directory. These
tests (also doctests) cover more corner cases and should include a set of
valid numbers that demonstrate that the module works correctly for real
numbers.

The normal tests should never require online sources for execution. All
functions that deal with online lookups (e.g. the EU VIES service for VAT
validation) should only be tested using conditional unittests.


Finding test numbers
--------------------

Some company numbers are commonly published on a company's website contact
page (e.g. VAT or other registration numbers, bank account numbers). Doing a
web search limited to a country and some key words generally turn up a lot of
pages with this information.

Another approach is to search for spreadsheet-type documents with some
keywords that match the number. This sometimes turns up lists of companies
(also occasionally works for personal identifiers).

For information that is displayed on ID cards or passports it is sometimes
useful to do an image search.

For dealing with numbers that point to individuals it is important to:

* Only keep the data that is needed to test the implementation.
* Ensure that no actual other data relation to a person or other personal
  information is kept or can be inferred from the kept data.
* The presence of a number in the test set should not provide any information
  about the person (other than that there is a person with the number or
  information that is present in the number itself).

Sometimes numbers are part of a data leak. If this data is used to pick a few
sample numbers from the selection should be random and the leak should not be
identifiable from the picked numbers. For example, if the leaked numbers
pertain only to people with a certain medical condition, membership of some
organisation or other specific property the leaked data should not be used.


Reverse engineering
-------------------

Sometimes a number format clearly has a check digit but the algorithm is not
publicly documented. It is sometimes possible to reverse engineer the used
check digit algorithm from a large set of numbers.

For example, given numbers that, apart from the check digit, only differ in
one digit will often expose the weights used. This works reasonably well if
the algorithm uses modulo 11 is over a weighted sums over the digits.

See https://github.com/arthurdejong/python-stdnum/pull/203#issuecomment-623188812


Registries
----------

Some numbers or parts of numbers use validation base on a registry of known
good prefixes, ranges or formats. It is only useful to fully base validation
on these registries if the update frequency to these registries is very low.

If there is a registry that is used (a list of known values, ranges or
otherwise) the downloaded information should be stored in a data file (see
the stdnum.numdb module). Only the minimal amount of data should be kept (for
validation or identification).

The data files should be able to be created and updated using a script in the
`update` directory.
