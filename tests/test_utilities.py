import unittest
from lxml import etree as et
from src.quickbooks_desktop.utilities import encode_special_characters


class TestEncodeSpecialCharacters(unittest.TestCase):
    def test_basic_replacement(self):
        # Test replacing common special characters
        input_str = "Hello & World"
        expected_output = "Hello &amp; World"
        actual_output = encode_special_characters(input_str)
        self.assertEqual(actual_output, expected_output)

        input_str = "Quotes: \" and '"
        expected_output = "Quotes: &quot; and &apos;"
        self.assertEqual(encode_special_characters(input_str), expected_output)

        input_str = "Special: ñ Ñ"
        expected_output = "Special: &#241; &#209;"
        self.assertEqual(encode_special_characters(input_str), expected_output)

    def test_preserve_valid_entities(self):
        # Test that valid numeric and named entities are preserved
        input_str = "Valid entity: &#241; &amp; &quot;"
        expected_output = "Valid entity: &#241; &amp; &quot;"
        self.assertEqual(encode_special_characters(input_str), expected_output)

    def test_mixed_input(self):
        # Test a mix of replaceable and valid entities
        input_str = "Mix: & Hello &#241; ñ &amp; &"
        expected_output = "Mix: &amp; Hello &#241; &#241; &amp; &amp;"
        actual_output = encode_special_characters(input_str)
        self.assertEqual(actual_output, expected_output)

    def test_no_special_characters(self):
        # Test strings without special characters
        input_str = "Plain text"
        expected_output = "Plain text"
        self.assertEqual(encode_special_characters(input_str), expected_output)

    def test_empty_string(self):
        # Test empty input
        input_str = ""
        expected_output = ""
        self.assertEqual(encode_special_characters(input_str), expected_output)

