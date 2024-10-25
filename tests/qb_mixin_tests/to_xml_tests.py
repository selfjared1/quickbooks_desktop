import unittest
from decimal import Decimal
import xml.etree.ElementTree as et
from dataclasses import dataclass, field, fields, is_dataclass
from typing import List, Optional, Any
from src.quickbooks_desktop.mixins.qb_mixins import ToXmlMixin
from src.quickbooks_desktop.common import LinkedTxn
from src.quickbooks_desktop.qb_special_fields import QBDates
from datetime import datetime

# Sample dataclass to use with ToXmlMixin
@dataclass
class TestData(ToXmlMixin):
    name: str = field(metadata={"name": "Name"})
    is_active: bool = field(metadata={"name": "IsActive"})
    items: List[str] = field(default_factory=list, metadata={"name": "Items"})
    description: Optional[str] = field(default=None, metadata={"name": "Description"})

    class Meta:
        name = "TestData"


# Unit test class for ToXmlMixin
class TestToXmlMixin(unittest.TestCase):

    def test_to_xml_simple(self):
        data = TestData(name="TestName", is_active=True, items=["item1", "item2"], description="A description")
        xml_element = data.to_xml()

        # Assert root element
        self.assertEqual(xml_element.tag, "TestData")

        # Assert child elements
        self.assertEqual(xml_element.find("Name").text, "TestName")
        self.assertEqual(xml_element.find("IsActive").text, "true")
        self.assertEqual(xml_element.find("Description").text, "A description")

        # Assert list elements
        items_element = xml_element.find("Items")
        self.assertIsNotNone(items_element)
        self.assertEqual(len(items_element), 2)
        self.assertEqual(items_element[0].text, "item1")
        self.assertEqual(items_element[1].text, "item2")

    def test_to_xml_with_no_field_order(self):
        data = TestData(name="TestName", is_active=False, items=["item1", "item2"], description=None)
        xml_element = data.to_xml()

        # Test order based on field definition when FIELD_ORDER is not present
        elements = list(xml_element)
        self.assertEqual(elements[0].tag, "Name")
        self.assertEqual(elements[1].tag, "IsActive")
        self.assertEqual(elements[2].tag, "Items")

    def test_to_xml_with_field_order(self):
        # Add FIELD_ORDER to the dataclass
        TestData.FIELD_ORDER = ["is_active", "name", "items", "description"]
        data = TestData(name="TestName", is_active=True, items=["item1"], description="Test description")
        xml_element = data.to_xml()

        # Test order based on FIELD_ORDER
        elements = list(xml_element)
        self.assertEqual(elements[0].tag, "IsActive")
        self.assertEqual(elements[1].tag, "Name")
        self.assertEqual(elements[2].tag, "Items")
        self.assertEqual(elements[3].tag, "Description")

    def test_to_xml_with_boolean_true(self):
        data = TestData(name="TestName", is_active=True, items=[], description=None)
        xml_element = data.to_xml()
        self.assertEqual(xml_element.find("IsActive").text, "true")

    def test_to_xml_with_boolean_false(self):
        data = TestData(name="TestName", is_active=False, items=[], description=None)
        xml_element = data.to_xml()
        self.assertEqual(xml_element.find("IsActive").text, "false")

    def test_to_xml_with_yes_no_boolean(self):
        # Add "IsActive" to the IS_YES_NO_FIELD_LIST to test Yes/No handling
        TestData.IS_YES_NO_FIELD_LIST = ["IsActive"]
        data = TestData(name="TestName", is_active=True, items=[], description=None)
        xml_element = data.to_xml()
        self.assertEqual(xml_element.find("IsActive").text, "Yes")

        data.is_active = False
        xml_element = data.to_xml()
        self.assertEqual(xml_element.find("IsActive").text, "No")


class TestToXmlMixin(unittest.TestCase):

    def setUp(self):
        # Create an instance of the class you're testing
        self.obj = ToXmlMixin()

        # Define the field that will be passed to the _handle_list_value
        self.field = type('Field', (object,), {
            'name': 'linked_txn',
            'metadata': {'name': 'LinkedTxn'}
        })()

        # Create the exact value_list you provided
        self.value_list = [
            LinkedTxn(
                txn_id='1043-1071523943',
                txn_type='ReceivePayment',
                txn_date=QBDates(date=datetime(2023, 8, 25, 0, 0)),
                ref_number=None,
                link_type='AMTTYPE',
                amount=Decimal('-480.00'),
                txn_line_detail=[]
            )
        ]

    def test_handle_list_value(self):
        root = et.Element('Invoice')

        # Call the method with the exact value_list you provided
        element = self.obj._handle_list_value(root, self.field, self.value_list)

        # Check if the element is created correctly
        self.assertIsNotNone(element)
        self.assertEqual(element.tag, 'LinkedTxn')
        self.assertEqual(len(element), 1)  # One linked transaction

        # Check the child elements inside LinkedTxn
        txn_id = element[0].find('TxnID').text
        self.assertEqual(txn_id, '1043-1071523943')
        txn_type = element[0].find('TxnType').text
        self.assertEqual(txn_type, 'ReceivePayment')
        link_type = element[0].find('LinkType').text
        self.assertEqual(link_type, 'AMTTYPE')
        amount = element[0].find('Amount').text
        self.assertEqual(amount, '-480.00')


if __name__ == "__main__":
    unittest.main()
