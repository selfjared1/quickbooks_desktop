import unittest
from core.mixins import QBMetaData


class TestQBMetaData(unittest.TestCase):
    def test_initialization(self):
        """ Test that initial attributes are set to empty strings """
        metadata = QBMetaData()
        self.assertEqual(metadata.TimeCreated, "")
        self.assertEqual(metadata.TimeModified, "")
        self.assertEqual(metadata.EditSequence, "")