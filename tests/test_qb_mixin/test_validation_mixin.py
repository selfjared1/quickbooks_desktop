import unittest
from dataclasses import dataclass, field
from typing import List, Optional
from src.quickbooks_desktop.qb_objects import ValidationMixin

# Re-defining ValidationMixin after kernel reset

# Sample dataclass using the mixin
VALID_OPTIONS = ["OptionA", "OptionB", "OptionC"]

@dataclass
class SampleValidatedModel(ValidationMixin):
    single_value: Optional[str] = field(
        default=None,
        metadata={"valid_values": VALID_OPTIONS}
    )
    list_value: List[str] = field(
        default_factory=list,
        metadata={"valid_values": VALID_OPTIONS}
    )

# Unit tests
class TestValidationMixin(unittest.TestCase):

    def test_valid_single_value(self):
        obj = SampleValidatedModel(single_value="OptionA")
        self.assertEqual(obj.single_value, "OptionA")

    def test_invalid_single_value_raises(self):
        with self.assertRaises(ValueError):
            SampleValidatedModel(single_value="Invalid")

    def test_valid_list_value(self):
        obj = SampleValidatedModel(list_value=["OptionA", "OptionB"])
        self.assertEqual(obj.list_value, ["OptionA", "OptionB"])

    def test_invalid_list_value_raises(self):
        with self.assertRaises(ValueError):
            SampleValidatedModel(list_value=["OptionA", "Invalid"])

    def test_runtime_update_invalid_value_raises(self):
        obj = SampleValidatedModel(single_value="OptionA")
        with self.assertRaises(ValueError):
            obj.single_value = "Invalid"

    def test_runtime_update_valid_value(self):
        obj = SampleValidatedModel()
        obj.single_value = "OptionC"
        self.assertEqual(obj.single_value, "OptionC")

    def test_runtime_update_invalid_list_item(self):
        obj = SampleValidatedModel()
        with self.assertRaises(ValueError):
            obj.list_value = ["Invalid", "OptionA"]

    def test_runtime_update_valid_list(self):
        obj = SampleValidatedModel()
        obj.list_value = ["OptionB"]
        self.assertEqual(obj.list_value, ["OptionB"])


