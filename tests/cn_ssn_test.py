import unittest

from stdnum.cn import ric
from stdnum.exceptions import ValidationError


VALID_SSN = ['486268198802140611', '354133198209290022', '338720197801060214',
   '387908198001010226', '341617198002120424', '38064219921117061X',
   '45883019880120031X']


class TestChinaRic(unittest.TestCase):
    def test_non_digit(self):
        try:
            ric.validate('It is a bad SSN')
            self.assertTrue(False, 'Should throw ValidationError')
        except ValidationError:
            self.assertTrue(True, 'Should throw ValidationError')

    def test_valid(self):
        for number in VALID_SSN:
            ric.validate(number)
            self.assertTrue(ric.is_valid(number))

    def test_invalid_checksum(self):
        for num in VALID_SSN:
            checksum = num[-1:]

            for n in range(0, 10):
                if str(n) == checksum:
                    continue
                number = num[:-1] + str(n)
                self.assertFalse(ric.is_valid(number))
                try:
                    ric.validate(number)
                    self.assertTrue(False, 'Should throw ValidationError')
                except ValidationError:
                    self.assertTrue(True, 'Should throw ValidationError')
