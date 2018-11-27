import unittest

from stdnum.no import ssn
from stdnum.exceptions import ValidationError


VALID_SSN = (
    ('42957044500', 1),
    ('11027794191', 1),
    ('31042639152', 1),
    ('71946503120', 1),
    ('95700625908', 1),
    ('68413152112', 1),
    ('56653047547', 1),
    ('70624830529', 1),
    ('75442702381', 1),
    ('34831582121', 1),
    ('27389446152', 1),
    ('96517753502', 1),
    ('46929323343', 1),
    ('92782833709', 1),
    ('40070897972', 1),
    ('56403643756', 1),
    ('24396859900', 1),
    ('89829529360', 1),
    ('30383131118', 1),
    ('30777674125', 1),
    ('71494457037', 0),
    ('83814827871', 0),
    ('40673759612', 0),
    ('44207789809', 0),
    ('70341666064', 0),
    ('11051996811', 0),
    ('39043009846', 0),
    ('27213364885', 0),
    ('70031073454', 0),
    ('42115114470', 0),
    ('19575770838', 0),
    ('50067834221', 0),
    ('63282310041', 0),
    ('42485176432', 0),
    ('98576936818', 0),
    ('79318270827', 0),
    ('21918484865', 0),
    ('79189404641', 0),
    ('82938389280', 0),
    ('45014054018', 0),
)


class TestNorwaySSN(unittest.TestCase):
    def test_non_digit(self):
        try:
            ssn.validate('It is a bad SSN')
            self.assertTrue(False, 'Should throw ValidationError')
        except ValidationError:
            self.assertTrue(True, 'Should throw ValidationError')

    def test_valid(self):
        for number, _ in VALID_SSN:
            ssn.validate(number)
            self.assertTrue(ssn.is_valid(number))

    def test_valid_gender(self):
        # 1 - Male, 0 - Female
        for number, gender in VALID_SSN:
            self.assertTrue(ssn.is_valid(number, gender))
            self.assertFalse(ssn.is_valid(number, 0 if gender else 1))

    def test_invalid_checksum(self):
        def check_number(number, gender):
            self.assertFalse(ssn.is_valid(number))
            self.assertFalse(ssn.is_valid(number, 0 if gender else 1))
            self.assertFalse(ssn.is_valid(number, gender))

        for num, gender in VALID_SSN:
            checksum = int(num[-2:])

            for n in xrange(0, 100):
                if n == checksum:
                    continue
                number = num[:-2] + '%02d' % n
                check_number(number, gender)
