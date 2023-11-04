import unittest
import pandas as pd
import datetime as dt
from core.special_fields import QBDate

class TestQBDates(unittest.TestCase):

    def test_check_date_not_none(self):
        with self.assertRaises(Exception) as context:
            QBDate()
        self.assertEqual(str(context.exception), 'You did not include a date')

    def test_parse_date_with_macro(self):
        qb_date = QBDate('today')
        self.assertEqual(qb_date.date, 1)
        self.assertEqual(qb_date.is_macro, True)

        qb_date = QBDate('next_year')
        self.assertEqual(qb_date.date, 23)
        self.assertEqual(qb_date.is_macro, True)

        with self.assertRaises(Exception):
            qb_date = QBDate('not_a_date')

    def test_parse_date_with_string(self):
        qb_date = QBDate('01/01/2000')
        self.assertEqual(qb_date.date, '01/01/2000')
        self.assertEqual(qb_date.is_macro, False)

    def test_parse_common_python_date_formats(self):
        date_to_parse = dt.datetime.now()
        qb_date = QBDate(date_to_parse)
        self.assertEqual(qb_date.date, date_to_parse.strftime('%m/%d/%Y'))

        date_to_parse = dt.date.today()
        qb_date = QBDate(date_to_parse)
        self.assertEqual(qb_date.date, date_to_parse.strftime('%m/%d/%Y'))

        date_to_parse = pd.Timestamp('2022-01-01')
        qb_date = QBDate(date_to_parse)
        self.assertEqual(qb_date.date, date_to_parse.strftime('%m/%d/%Y'))
