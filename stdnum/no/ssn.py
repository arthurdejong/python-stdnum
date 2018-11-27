# coding: utf-8

from stdnum.util import clean
from stdnum.exceptions import *


class PersonNumber(object):
    mapping = {
        0: 'd1',
        1: 'd2',
        2: 'm1',
        3: 'm2',
        4: 'y1',
        5: 'y2',
        6: 'i1',
        7: 'i2',
        8: 'i3',
        9: 'k1',
        10: 'k2'
    }

    def __init__(self, number_str):
        self.number_str = number_str
        for index, item in self.mapping.items():
            setattr(self, item, int(number_str[index]))

    def validate(self, gender=None):
        n = self
        if gender is not None and n.i3 % 2 != gender:
            raise ValidationError('Gender check failed')

        checksum_1 = 11 - (((3 * n.d1) + (7 * n.d2) + (6 * n.m1) + (1 * n.m2) + (8 * n.y1) + (9 * n.y2) + (4 * n.i1) + (5 * n.i2) + (2 * n.i3)) % 11)
        if checksum_1 == 11:
            checksum_1 = 0

        checksum_2 = 11 - (((5 * n.d1) + (4 * n.d2) + (3 * n.m1) + (2 * n.m2) + (7 * n.y1) + (6 * n.y2) + (5 * n.i1) + (4 * n.i2) + (3 * n.i3) + (2 * checksum_1)) % 11)
        if checksum_2 == 11:
            checksum_2 = 0

        if n.k1 == checksum_1 and n.k2 == checksum_2:
            return self.number_str
        else:
            raise ValidationError


def validate(number, gender=None):
    """Check if the number is a valid Norwegian PersonNumber."""
    number = clean(number, ' -:')
    if len(number) != 11:
        raise InvalidLength
    if not number.isdigit():
        raise InvalidFormat
    return PersonNumber(number).validate(gender)


def is_valid(number, gender=None):
    try:
        return bool(validate(number, gender))
    except ValidationError:
        return False
