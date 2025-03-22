import unittest
from lxml import etree as et
from src.quickbooks_desktop.qb_special_fields import QBDatesMacro



class TestQBDateMacro(unittest.TestCase):

    def setUp(self):
        self.qb_date_macro = QBDatesMacro()

    def test_date_getter(self):
        self.qb_date_macro.date = 'today'
        self.assertEqual(self.qb_date_macro.date, 1)

    def test_date_getter_no_date_provided(self):
        with self.assertRaises(ValueError):
            self.qb_date_macro.date = None

    def test_date_getter_incorrect_macro_provided(self):
        with self.assertRaises(ValueError):
            self.qb_date_macro.date = 'not_existing_macro'

    def test_date_setter(self):
        self.qb_date_macro.date = 'next_month'
        self.assertEqual(self.qb_date_macro._date, 21)

    def test_get_macro_dict(self):
        macro_dict = QBDatesMacro.get_macro_dict()
        self.assertEqual(macro_dict['next_month'], 21)

    def test_to_xml(self):
        field_name = 'ReportDateMacro'
        self.qb_date_macro.date = "today"
        date_xml = self.qb_date_macro.to_xml(field_name)
        self.assertTrue('Reportdatemacro' in date_xml.tag)

    def test_from_xml(self):
        element = et.Element('test_element')
        element.text = 'rdmlastmonth'
        qb_date_macro = QBDatesMacro.from_xml(element)
        self.assertEqual(qb_date_macro._date, 13)

    def test_to_string_macro_value(self):
        self.qb_date_macro.date = 'today'
        self.assertEqual(self.qb_date_macro.date, 1)


