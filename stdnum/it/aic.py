# This file is based on code from pyAIC, a Python library to work
# with AIC codes for drugs.
# https://github.com/FabrizioMontanari/pyAIC


"""
A series of function to manipulate, convert and (syntactically) validate
AIC codes as described in the italian
"Gazzetta Ufficiale della Repubblica Italiana" Serie Generale
n.165 del 18-07-2014, attachment A.
The document describes two valid representation of an AIC code.
This module,aside from standard compact, is_valid and validate provides some extra
utility functions:
- is_base10_AIC(code), to check if code is a valid base10 representation;
- is_base32_AIC(code), to check if code is a valid base32 representation;
- to_base32(code), to convert a base10 code to a base32 one (does not perform checks);
- to_from32(code), to convert a base32 code to a base10 one (does not perform checks);

This module also expose two function to convert a code between
base32 and base10 representation and vice versa.
"""
from stdnum.exceptions import *
from stdnum.util import clean

# the table of AIC base32 allowed chars.
AIC_TABLE = '0123456789BCDFGHJKLMNPQRSTUVWXYZ'


def from_base32(string):
    """Convert a base32 representation of an AIC to a base10 one.
    Parameters
    ----------
    string : str
        The string containing the base32 AIC
    Returns
    -------
    str
        The converted string. Returns None if it fails.
    """
    # reverse string
    string = string[::-1]
    tot = 0
    try:
        for idx, x in enumerate(string):
            tot = tot + AIC_TABLE.index(x.upper()) * 32 ** idx
    except ValueError:
        raise InvalidFormat()
    return str(tot).zfill(9)


def to_base32(string):
    """Convert a base10 representation of an AIC to a base32 one.
    Parameters
    ----------
    string : str
        The string containing the base10 AIC
    Returns
    -------
    str
        The converted string.
    """
    res = ''
    remainder = int(string)
    while remainder > 31:
        char = AIC_TABLE[remainder % 32]
        remainder = remainder // 32
        res = res + char
    res = res + AIC_TABLE[remainder]
    res = res[::-1]
    return res.zfill(6)

def calc_check_digit(aic):
    """Calculate the check digit for the BASE10 AIC code."""
    # p = sum(map(lambda x: (2 * int(aic[x])) // 10 + (2 * int(aic[x])) % 10,
    #             (1, 3, 5, 7)))
    # d = sum([ int(aic[x]) for x in (0, 2, 4, 6)])
    # return str((d + p) % 10)
    ## x // 10 == 0 since x is one char
    ## x % 10 == x since x is one char
    weights = (1, 2, 1, 2, 1, 2, 1, 2)
    return str(sum((x // 10) + (x % 10) for x in (w * int(n) for w, n in zip(weights, aic))) % 10)


def check_base10_checksum(aic):
    """Check if a string checksum char in the base10 representation is correct.
    Parameters
    ----------
    aic : str
        The string containing the code to check
    Returns
    -------
    bool
        True if the checksum is correct.
    """
    char = calc_check_digit(aic)
    return aic[-1] == char


def is_base10(code):
    """Check if a string is a valid base10 representation of an AIC code.
    Parameters
    ----------
    code : str
        The string containing the code to check
    Returns
    -------
    bool
        True if the code is syntactically correct.
    """
    if len(code) != 9:
        raise InvalidLength()
    for c in code:
        if c.lower() not in AIC_TABLE[:10]:
            raise InvalidFormat()
    if code[0] != '0':
        raise InvalidFormat()
    res = check_base10_checksum(code)
    if not res:
        raise InvalidChecksum()
    return res


def is_base32(code):
    """Check if a string is a valid base32 representation of an AIC code.
    Parameters
    ----------
    code : str
        The string containing the code to check
    Returns
    -------
    bool
        True if the code is syntactically correct.
    """
    if len(code) != 6:
        raise InvalidLength()
    for c in code:
        if c.lower() not in AIC_TABLE:
            raise InvalidFormat()
    # we can safelly convert to base10
    converted = from32to10(code)
    # the base 32 is valid if its base 10 is valid
    # using base 10 we can perform an extra check on the checksum digit
    return is_base10(converted)

def compact(code):
    """Convert the number to the minimal representation. This removes
    surrounding whitespace and makes chars uppercase."""
    if not isinstance(code, str):
        raise InvalidFormat()
    cleaned = clean(code, ' ').upper().strip()
    return cleaned


def validate(code):
    """Check if a string is a valid AIC. Base10 is the canonical form and
       is 9 chars long, while base32 is 6 chars. 
    Parameters
    ----------
    code : str
        The string containing the code to check
    Returns
    -------
    bool
        True if the code is a valid base32 or base10 representation
        of an AIC code.
    """
    code = compact(code)
    
    if len(code) == 6:
        #base32 length
        return is_base32(code)
    else:
        return is_base10(code)

def is_valid(code):
    """Check if the given string is a valid AIC code."""
    try:
        return bool(validate(code))
    except ValidationError:
        return False
