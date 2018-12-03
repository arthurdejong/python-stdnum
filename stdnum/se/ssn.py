# coding: utf-8
"""
Validation for Swedish SSN
https://en.wikipedia.org/wiki/Personal_identity_number_(Sweden)
"""
from stdnum import luhn
from stdnum.exceptions import *
from stdnum.util import clean


def validate(number):  # noqa
    number = clean(number, ' -+:')
    if len(number) != 10:
        raise InvalidLength()
    if not number.isdigit():
        raise InvalidFormat()
    return luhn.validate(number)


def is_valid(number):  # noqa
    try:
        return bool(validate(number))
    except ValidationError:
        return False
