"""
Provide tests for German Steuernummer (Tax number)
"""
from unittest import TestCase
from mock import Mock, patch
from stdnum.exceptions import (
    InvalidFormat,
    InvalidLength
)
from stdnum.de.StNr import (
    get_state_opening_characters,
    check_number_acceptable_to_state,
    validate,
    compact,
    validate_bund_schema,
    validate_standard_schema
)


class TestDeStNr(TestCase):
    """Tests for the module methods"""
    def test_get_opening_chars(self):
        """
        Test that the function returns the opening chars for available state
        and schema.
        """
        expected_chars = '11'
        opening_chars = get_state_opening_characters(
            state='Berlin',
            schema='bund'
        )
        self.assertEqual(expected_chars, opening_chars)

    def test_get_opening_chars_invalid_input(self):
        """
        Test that the method raises and exception when state or schema provided
        is not valid.
        """
        with self.assertRaises(KeyError) as _:
            get_state_opening_characters(
                state='Berln',
                schema='bund'
            )

        with self.assertRaises(KeyError) as _:
            get_state_opening_characters(
                state='Berlin',
                schema='bond'
            )

    def test_check_number_acceptable_to_state(self):
        """Test the main functionality of the method"""
        acceptable_number = '1123456789'
        self.assertTrue(
            check_number_acceptable_to_state(
                number=acceptable_number,
                state='Berlin',
                schema='bund'
            )
        )
        unacceptable_number = '1223456789'
        with self.assertRaises(InvalidFormat) as _:
            check_number_acceptable_to_state(
                number=unacceptable_number,
                state='Berlin',
                schema='bund'
            )

    def test_compact(self):
        """Test the compact functionality"""
        original_number = '122-1234-1234'
        expected_compact = '12212341234'
        self.assertEqual(compact(original_number), expected_compact)

        original_number_diff_format = '122/1234/1234'
        self.assertEqual(
            compact(original_number_diff_format), expected_compact
        )

    def test_validate_bund_schema(self):
        """Test the Bundesschema validator"""
        validated = validate_bund_schema('112304', 'Berlin')
        self.assertEqual(validated, '112304')

    def test_validate_invalid_bund_schema(self):
        """Test the Bundesschema validator for invalid number"""
        with self.assertRaises(InvalidFormat) as _:
            validate_bund_schema('11234', 'Berlin')

    def test_validate_standard_schema(self):
        """Test the Standardschema validator"""
        validated = validate_standard_schema('011234', 'Brandenburg')
        self.assertEqual(validated, '011234')

    def test_validate_invalid_standard_schema(self):
        """Test the Standardschema validator"""
        with self.assertRaises(InvalidFormat) as _:
            validate_standard_schema('211234', 'Brandenburg')

    def test_validate_without_state(self):
        """
        validate method should be able to validate without the state if
        called. The checks should be based on length of the number
        """
        first_valid_number = '1234567890'  # 10 digits.
        second_valid_number = '12345678901'  # 11 digits.
        third_valid_number = '1234056789012'  # 13 digits
        self.assertTrue(validate(first_valid_number), first_valid_number)
        self.assertTrue(validate(second_valid_number), second_valid_number)
        self.assertTrue(validate(third_valid_number), third_valid_number)

    def test_validate_invalid_length(self):
        """Validating invalid length should raise an exception"""
        with self.assertRaises(InvalidLength) as _:
            short_number = '123456789'
            validate(short_number)

    @patch('stdnum.de.StNr.validate_bund_schema')
    def test_validate_with_state_bund_schema(self, mock_validate_bund_schema):
        """if state is provided, state validation logic should be invoked"""
        number = '1034056789012'
        state = 'Saarland'
        validate(number=number, state=state)
        self.assertTrue(mock_validate_bund_schema.called)
        call_num, call_state = mock_validate_bund_schema.call_args[0]
        self.assertEqual(call_num, number)
        self.assertEqual(state, call_state)

    @patch('stdnum.de.StNr.validate_standard_schema')
    def test_validate_with_state_standard_schema(self,
                                                 mock_validate_stand_schema):
        """if state is provided, state validation logic should be invoked"""
        number = '1234567890'
        state = 'Saarland'
        validate(number=number, state=state)
        self.assertTrue(mock_validate_stand_schema.called)
        call_num, call_state = mock_validate_stand_schema.call_args[0]
        self.assertEqual(call_num, number)
        self.assertEqual(state, call_state)
