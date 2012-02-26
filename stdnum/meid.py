# meid.py - functions for handling Mobile Equipment Identifiers (MEIDs)
#
# Copyright (C) 2010, 2011, 2012 Arthur de Jong
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

"""MEID (Mobile Equipment Identifier).

The Mobile Equipment Identifier is used to identify a physical piece of
CDMA mobile station equipment.

>>> compact('AF 01 23 45 0A BC DE C')
'AF0123450ABCDE'
>>> is_valid('AF 01 23 45 0A BC DE')
True
>>> is_valid('AF 01 23 45 0A BC DE C')
True
>>> is_valid('29360 87365 0070 3710 0')
True
>>> format('af0123450abcDEC', add_check_digit=True)
'AF 01 23 45 0A BC DE C'
"""

from stdnum.util import clean


_hex_alphabet = '0123456789ABCDEF'


def _cleanup(number):
    """Remove any grouping information from the number and removes surrounding
    whitespace."""
    return clean(str(number), ' -').strip().upper()


def _ishex(number):
    for x in number:
        if x not in _hex_alphabet:
            return False
    return True


def _parse(number):
    number = _cleanup(number)
    if len(number) == 14 and _ishex(number):
        # 14-digit hex representation
        return number, ''
    elif len(number) == 15 and _ishex(number):
        # 14-digit hex representation with check digit
        return number[0:14], number[14]
    elif len(number) == 18 and number.isdigit():
        # 18-digit decimal representation
        return number, ''
    elif len(number) == 19 and number.isdigit():
        # 18-digit decimal representation witch check digit
        return number[0:18], number[18]
    else:
        return None


def _calc_check_digit(number):
    # both the 18-digit decimal format and the 14-digit hex format
    # containing only decimal digits should use the decimal Luhn check
    from stdnum import luhn
    if number.isdigit():
        return luhn.calc_check_digit(number)
    else:
        return luhn.calc_check_digit(number, alphabet=_hex_alphabet)


def compact(number, strip_check_digit=True):
    """Convert the MEID number to the minimal (hexadecimal) representation.
    This strips grouping information, removes surrounding whitespace and
    converts to hexadecimal if needed. If the check digit is to be preserved
    and conversion is done a new check digit is recalculated."""
    # first parse the number
    number, cd = _parse(number)
    # strip check digit if needed
    if strip_check_digit:
        cd = ''
    # convert to hex if needed
    if len(number) == 18:
        number = '%08X%06X' % (int(number[0:10]), int(number[10:18]))
        if cd:
            cd = _calc_check_digit(number)
    # put parts back together again
    return number + cd


def is_valid(number):
    """Checks to see if the number provided is a valid MEID number."""
    from stdnum import luhn
    # first parse the number
    try:
        number, cd = _parse(number)
    except:
        return False
    # decimal format can be easily determined
    if len(number) == 18:
        return not cd or luhn.is_valid(number + cd)
    # if the remaining hex format is fully decimal it is an IMEI number
    if number.isdigit():
        from stdnum import imei
        return imei.is_valid(number + cd)
    # normal hex Luhn validation
    return not cd or luhn.is_valid(number + cd, alphabet=_hex_alphabet)


def format(number, separator=' ', format=None, add_check_digit=False):
    """Reformat the passed number to the standard format. The separator
    used can be provided. If the format is specified (either 'hex' or
    'dec') the number is reformatted in that format, otherwise the current
    representation is kept. If add_check_digit is True a check digit will
    be added if it is not present yet."""
    # first parse the number
    number, cd = _parse(number)
    # format conversions if needed
    if format == 'dec' and len(number) == 14:
        # convert to decimal
        number = '%010d%08d' % (int(number[0:8], 16), int(number[8:14], 16))
        if cd:
            cd = _calc_check_digit(number)
    elif format == 'hex' and len(number) == 18:
        # convert to hex
        number = '%08X%06X' % (int(number[0:10]), int(number[10:18]))
        if cd:
            cd = _calc_check_digit(number)
    # see if we need to add a check digit
    if add_check_digit and not cd:
        cd = _calc_check_digit(number)
    # split number according to format
    if len(number) == 14:
        number = [number[i * 2:i * 2 + 2]
                  for i in range(7)] + [cd]
    else:
        number = (number[:5], number[5:10], number[10:14], number[14:], cd)
    return separator.join(x for x in number if x)


def to_pseudo_esn(number):
    """Convert the provided MEID to a pseudo ESN (pESN). The ESN is returned
    in compact HEX representation."""
    import hashlib
    # get the SHA1 of the binary representation of the number
    s = hashlib.sha1(compact(number, strip_check_digit=True).decode('hex'))
    # return the last 6 digits of the hash prefixed with the reserved
    # manufacturer code
    return '80' + s.hexdigest()[-6:].upper()
