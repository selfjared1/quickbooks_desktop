import unittest
import datetime as dt
from dateutil import parser
from core.special_fields import QBDates  # Adjust the import based on your project structure

class TestQBDates(unittest.TestCase):

    def test_macro_handling(self):
        """Test that date macros are correctly identified and handled."""
        date = QBDates('rdmtoday')
        self.assertTrue(date.date_is_macro)
        self.assertEqual(date.date, date.get_macro_dict()['rdmtoday'])

    def test_date_parsing_from_string(self):
        """Test that valid date strings are parsed correctly."""
        test_date = '2023-05-07'
        expected_date = parser.parse(test_date)
        date = QBDates(test_date)
        self.assertEqual(date.date, expected_date)

    def test_date_parsing_from_datetime(self):
        """Test that datetime objects are handled correctly."""
        test_date = dt.datetime.now()
        date = QBDates(test_date)
        self.assertEqual(date.date, test_date)

    def test_date_parsing_from_date(self):
        """Test that date objects are converted to datetime at 23:59:59."""
        test_date = dt.date.today()
        expected_datetime = dt.datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
        date = QBDates(test_date)
        self.assertEqual(date.date, expected_datetime)

    def test_invalid_date_string(self):
        """Test that an invalid date string raises an exception."""
        with self.assertRaises(Exception) as context:
            QBDates("not a real date")
        self.assertIn('could not be parsed', str(context.exception))

    def test_invalid_integer_range(self):
        """Test that an invalid integer input raises an exception."""
        with self.assertRaises(Exception) as context:
            QBDates(25)  # Outside the valid range for hour-based macros
        self.assertIn('could not be parsed', str(context.exception))

    def test_valid_integer_range(self):
        """Test that valid integer inputs are accepted as macro indexes."""
        date = QBDates(10)
        self.assertTrue(date.date_is_macro)
        self.assertEqual(date.date, 10)