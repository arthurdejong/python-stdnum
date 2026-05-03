#!/bin/sh

# go to directory that this script resides in
cd "$(dirname "$0")"

set -x

# run the update scripts to generate data files
./at_postleitzahl.py > ../stdnum/at/postleitzahl.dat
./be_banks.py > ../stdnum/be/banks.dat
./cfi.py > ../stdnum/cfi.dat
./cn_loc.py > ../stdnum/cn/loc.dat
./eu_nace.py > ../stdnum/eu/nace.dat
./gs1_ai.py > ../stdnum/gs1_ai.dat
./iban.py > ../stdnum/iban.dat
./imsi.py > ../stdnum/imsi.dat
./isbn.py > ../stdnum/isbn.dat
./isil.py > ../stdnum/isil.dat
./my_bp.py > ../stdnum/my/bp.dat
./nz_banks.py > ../stdnum/nz/banks.dat
./oui.py > ../stdnum/oui.dat
