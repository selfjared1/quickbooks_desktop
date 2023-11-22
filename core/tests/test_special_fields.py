import unittest
import pandas as pd
import dateutil.parser as parser
import datetime as dt
from core.special_fields import QBDate, Ref, QBDateMacro

class TestQBDateMacro(unittest.TestCase):
    def setUp(self):
        self.qb_date_macro = QBDateMacro('today')

    def test_valid_macros(self):
        valid_macros = ['rdmtoday', 'this_month', 'last_year_to_date']
        for macro in valid_macros:
            with self.subTest(macro=macro):
                result = self.qb_date_macro.parse_date_macro(macro)
                self.assertIsNotNone(result)
                self.assertIn(macro.lower(), self.qb_date_macro.macro_dict)

    def test_invalid_macro(self):
        with self.assertRaises(Exception):
            self.qb_date_macro.parse_date_macro('invalid_macro')

    def test_case_insensitivity(self):
        macro = 'RdmToday'
        result = self.qb_date_macro.parse_date_macro(macro)
        self.assertEqual(result, self.qb_date_macro.macro_dict['rdmtoday'])

class TestQBDate(unittest.TestCase):
    def test_date_object(self):
        date = dt.date.today()
        qb_date = QBDate(date)
        self.assertEqual(qb_date.date, date)

    def test_datetime_object(self):
        datetime = dt.datetime.now()
        qb_date = QBDate(datetime)
        self.assertEqual(qb_date.date, datetime.date())

    def test_string_date(self):
        date_string = "11/22/2023"
        qb_date = QBDate(date_string)
        expected_date = parser.parse(date_string).date()
        self.assertEqual(qb_date.date, expected_date)

    def test_invalid_string_date(self):
        with self.assertRaises(Exception):
            QBDate("invalid date string")

    def test_none_date(self):
        with self.assertRaises(Exception):
            QBDate(None)

    def test_pandas_datetime64(self):
        pd_date = pd.Timestamp('2023-11-22')
        qb_date = QBDate(pd_date)
        expected_date = dt.date(2023, 11, 22)
        self.assertEqual(qb_date.date, expected_date)

class TestRef(unittest.TestCase):

    def test_to_xml(self):
        # Create a Ref instance with known values
        ref = Ref(
            ref_label="TestRef",
            id_name="TestID",
            ID="123",
            name_name="TestName",
            Name="Test Account"
        )

        # Generate the XML string
        xml_str = ref.to_xml()

        # Expected XML string
        expected_xml = "<TestRef>\n  <TestID>123</TestID>\n  <TestName>Test Account</TestName>\n</TestRef>\n"

        # Assert that the generated XML matches the expected XML
        self.assertEqual(xml_str, expected_xml)