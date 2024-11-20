import unittest
from lxml import etree as et
from src.quickbooks_desktop.utilities import clean_text


class TestCleanTextFunction(unittest.TestCase):
    def setUp(self):
        # This is the input XML element used for testing
        self.input_element = et.fromstring("""
            <Desc>ARTCO Screw Mandrel - 1/4&quot; Screw &#215; 1/4&quot; &#216; Shank</Desc>
        """)

    def test_clean_text_basic(self):
        # Run the clean_text function on the sample input element
        cleaned_element = clean_text(self.input_element)
        cleaned_text = et.tostring(cleaned_element, encoding='unicode', method='html')

        # Check if certain replacements are correctly made
        self.assertIn("ARTCO Screw Mandrel - 1/4\" Screw x 1/4\" dia Shank", cleaned_text)

    def test_special_characters_removed(self):
        # Ensure specific entities like &#215; and &#216; are replaced correctly
        cleaned_element = clean_text(self.input_element)
        cleaned_text = et.tostring(cleaned_element, encoding='unicode', method='html')

        # Check for replacements of &#215; (×) with "x" and &#216; (Ø) with "dia"
        self.assertNotIn("&#215;", cleaned_text)
        self.assertNotIn("&#216;", cleaned_text)
        self.assertIn("x", cleaned_text)
        self.assertIn("dia", cleaned_text)

    def test_unwanted_strings_removed(self):
        # Test if unwanted strings like '&lt;' and '&gt;' are removed
        input_element = et.fromstring("<Desc>&lt;Some text&gt;</Desc>")
        cleaned_element = clean_text(input_element)
        cleaned_text = et.tostring(cleaned_element, encoding='unicode', method='html')

        self.assertNotIn("&lt;", cleaned_text)
        self.assertNotIn("&gt;", cleaned_text)
        self.assertIn("Some text", cleaned_text)

    def test_html_unescape(self):
        # Ensure HTML-escaped entities are correctly converted
        input_element = et.fromstring("<Desc>ARTCO &quot;Mandrel&quot;</Desc>")
        cleaned_element = clean_text(input_element)
        cleaned_text = et.tostring(cleaned_element, encoding='unicode', method='html')

        # Check if HTML entity &quot; is unescaped to "
        self.assertIn('"Mandrel"', cleaned_text)

    def test_handling_unicode_normalization_01(self):
        # Test that characters are decomposed and normalized as expected
        input_element = et.fromstring("<Desc>Text with Ångström and Crème brûlée</Desc>")
        cleaned_element = clean_text(input_element)
        cleaned_text = et.tostring(cleaned_element, encoding='unicode', method='html')

        # Check if accented characters are replaced with non-accented versions
        self.assertIn("Angstrom", cleaned_text)
        self.assertIn("Creme brulee", cleaned_text)

    def test_handling_unicode_normalization_02(self):
        # Test that characters are decomposed and normalized as expected
        input_element = et.fromstring("<FullName>Electric Motors &amp; Spindles:NR-3060S-C</FullName>")
        cleaned_element = clean_text(input_element)
        cleaned_text = et.tostring(cleaned_element, encoding='unicode', method='html')

        # Check if accented characters are replaced with non-accented versions
        self.assertIn("Electric Motors &amp; Spindles", cleaned_text)
