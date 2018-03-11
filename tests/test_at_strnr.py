from unittest import TestCase
from stdnum.at.stnr import (
    validate,
    is_valid,
    get_all_codes_dict,
    validate_acceptable_opening_chars,
    validate_opening_chars_to_office
)
from stdnum.exceptions import (
    InvalidFormat,
    InvalidLength
)
acceptable_number_office = ('571234567', 'Klagenfurt')
unacceptable_number_office = ('571234567', 'Spittal Villach')
unacceaptable_length = '12345678'
unacceaptable_char = 'X123455678'
acceptable_number = '571234567'


class TestATStnr(TestCase):
    """Tests for the module methods"""
    def test_get_all_codes_dict(self):
        """All codes dict should return a dictionary of all the valid codes"""
        all_codes = get_all_codes_dict()
        self.assertEqual(len(all_codes), 39)

    def test_validate_acceptable_opening_chars(self):
        """The first two chars should be validated against the list of opening
        chars that we have for office"""
        unacceptable_number = '00XXXXXXX'
        self.assertEqual(
            validate_acceptable_opening_chars(acceptable_number),
            acceptable_number
        )
        with self.assertRaises(InvalidFormat) as _:
            validate_acceptable_opening_chars(unacceptable_number)

    def test_validate_opening_chars_to_office(self):
        """The first two chars should match the ofice if the office is provided
        """

        self.assertTrue(
            validate_opening_chars_to_office(*acceptable_number_office)
        )
        with self.assertRaises(InvalidFormat) as _:
            validate_opening_chars_to_office(*unacceptable_number_office)

    def test_validate(self):
        """Test the validate functionality"""
        with self.assertRaises(InvalidFormat) as _:
            validate(unacceaptable_char)
        with self.assertRaises(InvalidLength) as _:
            validate(unacceaptable_length)
        with self.assertRaises(InvalidFormat) as _:
            validate(*unacceptable_number_office)
        self.assertEqual(validate(acceptable_number), acceptable_number)
        self.assertEqual(
            validate(*acceptable_number_office), acceptable_number_office[0]
        )

    def test_is_valid(self):
        """Test the boolean interface"""
        self.assertTrue(is_valid(acceptable_number))
        self.assertTrue(is_valid(*acceptable_number_office))
        self.assertFalse(is_valid(*unacceptable_number_office))
