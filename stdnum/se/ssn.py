# coding: utf-8
"""
Validation for Swedish SSN
https://en.wikipedia.org/wiki/Personal_identity_number_(Sweden)
"""
from stdnum.exceptions import *
from stdnum.util import clean
from stdnum import luhn


def validate(number):
    number = clean(number, ' -+:')
    if len(number) != 10:
        raise InvalidLength
    if not number.isdigit():
        raise InvalidFormat
    return luhn.validate(number)


def is_valid(number):
    try:
        return bool(validate(number))
    except ValidationError:
        return False
