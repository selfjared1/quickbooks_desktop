import unittest
from dataclasses import dataclass, field
from src.quickbooks_desktop.mixins.qb_mixins import MaxLengthMixin


# Sample dataclass to test the mixin
@dataclass
class TestClass(MaxLengthMixin):
    name: str = field(default="", metadata={"max_length": 10})
    description: str = field(default="", metadata={"max_length": 50})
    age: int = field(default=0)  # No max_length constraint here

# Unit test class for MaxLengthMixin
class TestMaxLengthMixin(unittest.TestCase):

    def test_set_within_max_length(self):
        obj = TestClass()
        obj.name = "Short"  # Length is 5, should be fine
        self.assertEqual(obj.name, "Short")

    def test_set_exceeds_max_length(self):
        obj = TestClass()
        with self.assertRaises(ValueError) as context:
            obj.name = "ThisNameIsTooLong"  # Length is 16, exceeds max_length=10
        self.assertIn("exceeds the maximum allowed length of 10", str(context.exception))

    def test_no_max_length_constraint(self):
        obj = TestClass()
        obj.age = 123  # No max_length for age, should work fine
        self.assertEqual(obj.age, 123)

    def test_set_string_no_max_length(self):
        obj = TestClass()
        obj.description = "A brief description"  # Length is within the max_length=50
        self.assertEqual(obj.description, "A brief description")

    def test_set_non_string_value(self):
        obj = TestClass()
        obj.name = 12345  # Setting an integer, should work fine as it's not a string
        self.assertEqual(obj.name, 12345)

