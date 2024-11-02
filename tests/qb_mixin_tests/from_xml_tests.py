import unittest
from decimal import Decimal
from lxml import etree as et
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.quickbooks_desktop import (
    FromXmlMixin, CustomerRef, Invoice, InvoiceLine, JournalEntry,
)


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
                <Desc>Product</Desc>
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
                <Desc>Product Custom Description</Desc>
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
        self.assertEqual(instance.invoice_lines[1].desc, "Product Custom Description")

    def test_basic_from_xml_06(self):
        # Test case for a simple XML element matching defined fields
        journal_xml = """
                <JournalEntryRet>
                    <TxnID>19C72-1627671245</TxnID>
                    <TimeCreated>2021-07-30T12:54:05-07:00</TimeCreated>
                    <TimeModified>2022-01-31T15:33:12-07:00</TimeModified>
                    <EditSequence>1627671245</EditSequence>
                    <TxnNumber>34217</TxnNumber>
                    <TxnDate>2005-10-18</TxnDate>
                    <RefNumber>1</RefNumber>
                    <IsAdjustment>false</IsAdjustment>
                    <IsHomeCurrencyAdjustment>false</IsHomeCurrencyAdjustment>
                    <IsAmountsEnteredInHomeCurrency>false</IsAmountsEnteredInHomeCurrency>
                    <CurrencyRef>
                    <ListID>80000096-1622403877</ListID>
                    <FullName>US Dollar</FullName>
                    </CurrencyRef>
                    <ExchangeRate>1</ExchangeRate>
                    <JournalCreditLine>
                    <TxnLineID>19C73-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>80000015-1622404240</ListID>
                    <FullName>Notes - Sample, Inc.</FullName>
                    </AccountRef>
                    <Amount>210000.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalCreditLine>
                    <JournalDebitLine>
                    <TxnLineID>19C74-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>8000005D-1627666939</ListID>
                    <FullName>Automobiles</FullName>
                    </AccountRef>
                    <Amount>4500.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalDebitLine>
                    <JournalDebitLine>
                    <TxnLineID>19C75-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>8000005E-1627666939</ListID>
                    <FullName>Furniture &amp; Fixtures</FullName>
                    </AccountRef>
                    <Amount>2000.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalDebitLine>
                    <JournalDebitLine>
                    <TxnLineID>19C76-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>8000005C-1627666939</ListID>
                    <FullName>Inventory</FullName>
                    </AccountRef>
                    <Amount>203500.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalDebitLine>
                </JournalEntryRet>
                """
        element = et.fromstring(journal_xml)
        instance = JournalEntry.from_xml(element)

        self.assertEqual(len(instance.journal_credit_lines), 1)
        self.assertEqual(instance.journal_credit_lines[0].txn_line_id, "19C73-1627671245")


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

