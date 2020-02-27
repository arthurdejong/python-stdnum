# This file is based on code from pyAIC, a Python library to work
# with AIC codes for drugs.
# https://github.com/FabrizioMontanari/pyAIC


"""
A series of function to manipulate, convert and (syntactically) validate
AIC codes as described in the italian
"Gazzetta Ufficiale della Repubblica Italiana" Serie Generale
n.165 del 18-07-2014, attachment A.
The document describes two valid representation of an AIC code.
This module provides three function to validate a code:
- is_base10_AIC(code), to check if code is a valid base10 representation;
- is_base32_AIC(code), to check if code is a valid base32 representation;
- validate(code), to check if code is a valid base10 or base32 representation.

This module also expose two function to convert a code between
base32 and base10 representation and vice versa.
"""
# the table of AIC base32 allowed chars.
AIC_TABLE = '0123456789bcdfghjklmnpqrstuvwxyz'


def from32to10(string):
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
            tot = tot + AIC_TABLE.index(x.lower())*32**idx
    except ValueError:
        return None
    return str(tot).zfill(9)


def from10to32(string):
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

    res = ""
    remainder = int(string)
    while remainder > 31:
        char = AIC_TABLE[remainder%32].upper()
        remainder = remainder//32
        res = res + char
    res = res + AIC_TABLE[remainder].upper()
    res = res[::-1]
    if len(res) == 5:
        res = "0" + res
    return res


def check_AIC_base10_checksum(AIC):
    """Check if a string checksum char in the base10 representation is correct.
    Parameters
    ----------
    AIC : str
        The string containing the code to check
    Returns
    -------
    bool
        True if the checksum is correct.
    """

    xn = [2*int(AIC[i]) for i in (1,3,5,7)]
    p = 0
    for x in xn:
        p = p + (x // 10) + (x % 10)
    d = 0
    for i in (0,2,4,6):
        d = d + int(AIC[i])
    return AIC[-1] == str((p + d)%10)


def is_base10_AIC(code):
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

    if not isinstance(code, str):
        return False
    if len(code) != 9:
        return False
    for c in code:
        if c.lower() not in AIC_TABLE[:10]:
            return False
    if code[0] != "0":
        return False
    return check_AIC_base10_checksum(code)


def is_base32_AIC(code):
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

    if not isinstance(code, str):
        return False
    if len(code) != 6:
        return False
    for c in code:
        if c.lower() not in AIC_TABLE:
            return False
    # we can safelly convert to base10
    converted = from32to10(code)
    # the base 32 is valid if its base 10 is valid
    # using base 10 we can perform an extra check on the checksum digit
    return is_base10_AIC(converted)

def validate(code):
    """Check if a string is a valid AIC (base10 or base 32)
    Parameters
    ----------
    AIC : code
        The string containing the code to check
    Returns
    -------
    bool
        True if the code is a valid base32 or base10 representation
        of an AIC code.
    """
    return is_base10_AIC(code) or is_base32_AIC(code)
