import unittest
from decimal import Decimal
from lxml import etree as et
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.quickbooks_desktop import FromXmlMixin, CustomerRef, Invoice, InvoiceLine




@dataclass
class TestClass(FromXmlMixin):
    name: Optional[str] = field(default=None, metadata={"name": "Name"})
    value: Optional[int] = field(default=None, metadata={"name": "Value"})
    extra_data: Optional[str] = field(default=None, metadata={"name": "ExtraData"})


@dataclass
class NestedTestClass(FromXmlMixin):
    nested_name: Optional[str] = field(default=None, metadata={"name": "NestedName"})


@dataclass
class ListTestClass(FromXmlMixin):
    nested_items: List[NestedTestClass] = field(default_factory=list, metadata={"name": "NestedItems"})


class TestFromXmlMixin(unittest.TestCase):

    def test_basic_from_xml(self):
        # Test case for a simple XML element matching defined fields
        xml_str = """
        <TestClass>
            <Name>TestName</Name>
            <Value>123</Value>
        </TestClass>
        """
        element = et.fromstring(xml_str)
        instance = TestClass.from_xml(element)

        self.assertEqual(instance.name, "TestName")
        self.assertEqual(instance.value, 123)

    def test_basic_from_xml_02(self):
        # Test case for a simple XML element matching defined fields
        xml_str = """
        <TestClass>
            <Name>TestName</Name>
            <Value>123</Value>
        </TestClass>
        """
        element = et.fromstring(xml_str)
        instance = TestClass.from_xml(element)

        self.assertEqual(instance.name, "TestName")
        self.assertEqual(instance.value, 123)

    def test_basic_from_xml_03(self):
        # Test case for a simple XML element matching defined fields
        xml_str = """
        <CustomerRef>
              <ListID>80000001-1326159291</ListID>
              <FullName>Netelco, Incorporated</FullName>
        </CustomerRef>
        """
        element = et.fromstring(xml_str)
        instance = CustomerRef.from_xml(element)

        self.assertEqual(instance.list_id, "80000001-1326159291")
        self.assertEqual(instance.full_name, "Netelco, Incorporated")

    def test_basic_from_xml_04(self):
        # Test case for a simple XML element matching defined fields
        xml_str = """
                <InvoiceLine>
                    <TxnLineID>4-1326159535</TxnLineID>
                    <ItemRef>
                        <ListID>80000001-1326159384</ListID>
                        <FullName>Estimating</FullName>
                    </ItemRef>
                    <Desc>Seasons 52 Fire Alarm - Fire Lite</Desc>
                    <Quantity>1</Quantity>
                    <Rate>100.00</Rate>
                    <Amount>100.00</Amount>
                    <SalesTaxCodeRef>
                        <ListID>80000002-1326158429</ListID>
                        <FullName>Non</FullName>
                    </SalesTaxCodeRef>
                </InvoiceLine>
        """
        element = et.fromstring(xml_str)
        instance = InvoiceLine.from_xml(element)

        self.assertEqual(instance.txn_line_id, "4-1326159535")
        self.assertEqual(instance.amount, Decimal(100.00))


    def test_basic_from_xml_05(self):
        # Test case for a simple XML element matching defined fields
        xml_str = """
        <InvoiceRet>
            <InvoiceLineRet>
                <TxnLineID>3-1326159535</TxnLineID>
                <ItemRef>
                    <ListID>80000001-1326159384</ListID>
                    <FullName>Estimating</FullName>
                </ItemRef>
                <Desc>Washington ES Low Voltage/Fire Alarm Bid</Desc>
                <Quantity>1</Quantity>
                <Rate>100.00</Rate>
                <Amount>100.00</Amount>
                <SalesTaxCodeRef>
                    <ListID>80000002-1326158429</ListID>
                    <FullName>Non</FullName>
                </SalesTaxCodeRef>
            </InvoiceLineRet>
            <InvoiceLineRet>
                <TxnLineID>4-1326159535</TxnLineID>
                <ItemRef>
                <ListID>80000001-1326159384</ListID>
                <FullName>Estimating</FullName>
                </ItemRef>
                <Desc>Seasons 52 Fire Alarm - Fire Lite</Desc>
                <Quantity>1</Quantity>
                <Rate>100.00</Rate>
                <Amount>100.00</Amount>
                <SalesTaxCodeRef>
                <ListID>80000002-1326158429</ListID>
                <FullName>Non</FullName>
                </SalesTaxCodeRef>
            </InvoiceLineRet>
        </InvoiceRet>
        """
        element = et.fromstring(xml_str)
        instance = Invoice.from_xml(element)

        self.assertEqual(len(instance.invoice_lines), 2)
        self.assertEqual(instance.invoice_lines[0].txn_line_id, "3-1326159535")
        self.assertEqual(instance.invoice_lines[0].item_ref.full_name, "Estimating")

    def test__get_init_args(self):
        xml_str = """
        <InvoiceLine>
            <TxnLineID>3-1326159535</TxnLineID>
            <ItemRef>
                <ListID>80000001-1326159384</ListID>
                <FullName>Estimating</FullName>
            </ItemRef>
            <Desc>Washington ES Low Voltage/Fire Alarm Bid</Desc>
            <Quantity>1</Quantity>
            <Rate>100.00</Rate>
            <Amount>100.00</Amount>
            <SalesTaxCodeRef>
                <ListID>80000002-1326158429</ListID>
                <FullName>Non</FullName>
            </SalesTaxCodeRef>
        </InvoiceLine>
        """

        element = et.fromstring(xml_str)
        field_names = {field.metadata.get("name", field.name): field for field in InvoiceLine.__dataclass_fields__.values()}
        init_args = InvoiceLine._get_init_args(element, field_names)
        self.assertIn("desc", init_args)
        self.assertEqual(init_args["desc"], "Washington ES Low Voltage/Fire Alarm Bid")

    def test_handle_unexpected_field(self):
        # Test case where the XML contains an unexpected field
        xml_str = """
        <TestClass>
            <Name>TestName</Name>
            <Value>123</Value>
            <UnexpectedField>ExtraValue</UnexpectedField>
        </TestClass>
        """
        element = et.fromstring(xml_str)
        instance = TestClass.from_xml(element)

        self.assertEqual(instance.name, "TestName")
        self.assertEqual(instance.value, 123)
        self.assertTrue(hasattr(instance, "UnexpectedField"))
        self.assertEqual(instance.UnexpectedField, "ExtraValue")

    def test_nested_object_parsing(self):
        # Test case for nested dataclass parsing
        xml_str = """
        <ListTestClass>
            <NestedItems>
                <NestedName>Item1</NestedName>
            </NestedItems>
            <NestedItems>
                <NestedName>Item2</NestedName>
            </NestedItems>
        </ListTestClass>
        """
        element = et.fromstring(xml_str)
        instance = ListTestClass.from_xml(element)

        self.assertEqual(len(instance.nested_items), 2)
        self.assertEqual(instance.nested_items[0].nested_name, "Item1")
        self.assertEqual(instance.nested_items[1].nested_name, "Item2")

    def test_field_with_text_content(self):
        # Test case for an XML element with text content (for main field)
        xml_str = """
        <TestClass>SomeTextContent</TestClass>
        """
        element = et.fromstring(xml_str)
        instance = TestClass.from_xml(element)

        self.assertEqual(instance.name, "SomeTextContent")

    def test_list_field_parsing(self):
        # Test case for a list field
        xml_str = """
        <ListTestClass>
            <NestedItems>
                <NestedName>Item1</NestedName>
            </NestedItems>
            <NestedItems>
                <NestedName>Item2</NestedName>
            </NestedItems>
        </ListTestClass>
        """
        element = et.fromstring(xml_str)
        instance = ListTestClass.from_xml(element)

        self.assertEqual(len(instance.nested_items), 2)
        self.assertEqual(instance.nested_items[0].nested_name, "Item1")
        self.assertEqual(instance.nested_items[1].nested_name, "Item2")

    def test_is_yes_no_field(self):
        # Test case for a field in the IS_YES_NO_FIELD_LIST
        TestClass.IS_YES_NO_FIELD_LIST = ['value']

        xml_str = """
        <TestClass>
            <Name>TestName</Name>
            <Value>Yes</Value>
        </TestClass>
        """
        element = et.fromstring(xml_str)
        instance = TestClass.from_xml(element)

        self.assertEqual(instance.value, True)  # Since "Yes" should map to True
        TestClass.IS_YES_NO_FIELD_LIST = []  # Reset for other tests

