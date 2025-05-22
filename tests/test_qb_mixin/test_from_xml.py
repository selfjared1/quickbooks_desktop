import unittest
from decimal import Decimal
from lxml import etree as et
from dataclasses import dataclass, field
from typing import Optional, List
from src.quickbooks_desktop.quickbooks_desktop import (
    FromXmlMixin, CustomerRef, Invoice, InvoiceLine, JournalEntry, SalesOrder
)
from datetime import datetime


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

    def test_full_from_xml_01(self):
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

        self.assertEqual(instance.ref_number, '1')
        self.assertEqual(len(instance.journal_credit_lines), 1)
        self.assertEqual(instance.journal_credit_lines[0].txn_line_id, "19C73-1627671245")

        # Assertions for main JournalEntry attributes
        self.assertEqual(instance.txn_id, '19C72-1627671245')
        self.assertEqual(instance.time_created.datetime_value, datetime.fromisoformat('2021-07-30T12:54:05-07:00'))
        self.assertEqual(instance.time_modified.datetime_value, datetime.fromisoformat('2022-01-31T15:33:12-07:00'))
        self.assertEqual(instance.edit_sequence, '1627671245')
        self.assertEqual(instance.txn_number, '34217')
        self.assertEqual(instance.txn_date.__str__(), '2005-10-18')
        self.assertEqual(instance.ref_number, '1')
        self.assertFalse(instance.is_adjustment)
        self.assertFalse(instance.is_home_currency_adjustment)
        self.assertFalse(instance.is_amounts_entered_in_home_currency)
        self.assertEqual(instance.currency_ref.list_id, '80000096-1622403877')
        self.assertEqual(instance.currency_ref.full_name, 'US Dollar')
        self.assertEqual(instance.exchange_rate, 1)

        # Assertions for JournalCreditLine
        self.assertEqual(len(instance.journal_credit_lines), 1)
        self.assertEqual(instance.journal_credit_lines[0].txn_line_id, "19C73-1627671245")
        self.assertEqual(instance.journal_credit_lines[0].account_ref.list_id, "80000015-1622404240")
        self.assertEqual(instance.journal_credit_lines[0].account_ref.full_name, "Notes - Sample, Inc.")
        self.assertEqual(instance.journal_credit_lines[0].amount, 210000.00)
        self.assertEqual(instance.journal_credit_lines[0].memo, "original purchase")

        # Assertions for JournalDebitLines
        self.assertEqual(len(instance.journal_debit_lines), 3)

        self.assertEqual(instance.journal_debit_lines[0].txn_line_id, "19C74-1627671245")
        self.assertEqual(instance.journal_debit_lines[0].account_ref.list_id, "8000005D-1627666939")
        self.assertEqual(instance.journal_debit_lines[0].account_ref.full_name, "Automobiles")
        self.assertEqual(instance.journal_debit_lines[0].amount, 4500.00)
        self.assertEqual(instance.journal_debit_lines[0].memo, "original purchase")

        self.assertEqual(instance.journal_debit_lines[1].txn_line_id, "19C75-1627671245")
        self.assertEqual(instance.journal_debit_lines[1].account_ref.list_id, "8000005E-1627666939")
        self.assertEqual(instance.journal_debit_lines[1].account_ref.full_name, "Furniture & Fixtures")
        self.assertEqual(instance.journal_debit_lines[1].amount, 2000.00)
        self.assertEqual(instance.journal_debit_lines[1].memo, "original purchase")

        self.assertEqual(instance.journal_debit_lines[2].txn_line_id, "19C76-1627671245")
        self.assertEqual(instance.journal_debit_lines[2].account_ref.list_id, "8000005C-1627666939")
        self.assertEqual(instance.journal_debit_lines[2].account_ref.full_name, "Inventory")
        self.assertEqual(instance.journal_debit_lines[2].amount, 203500.00)
        self.assertEqual(instance.journal_debit_lines[2].memo, "original purchase")

    def test_from_xml_so_lines(self):
        LINES_XML = """<?xml version="1.0" ?>
        <QBXML>
            <QBXMLMsgsRs>
                <SalesOrderQueryRs requestID="1" statusCode="0" statusSeverity="Info" statusMessage="Status OK">
                    <SalesOrderRet>
                        <TxnID>1DB9A-1745622547</TxnID>
                        <SalesOrderLineRet>
                            <TxnLineID>1DB9C-1745622547</TxnLineID>
                            <ItemRef>
                                <ListID>80000839-1737761486</ListID>
                                <FullName>Lotion Pump:ABF.64894547.JLP</FullName>
                            </ItemRef>
                            <Desc>Pump OLLY BW 28-410 JL-AMA\n\n                        PART #64894547</Desc>
                            <Quantity>300000</Quantity>
                            <Rate>0.15</Rate>
                            <Amount>45000.00</Amount>
                            <SalesTaxCodeRef>
                                <ListID>80000002-1693363606</ListID>
                                <FullName>Non</FullName>
                            </SalesTaxCodeRef>
                            <Invoiced>0</Invoiced>
                            <IsManuallyClosed>false</IsManuallyClosed>
                        </SalesOrderLineRet>
                        <SalesOrderLineRet>
                            <TxnLineID>1DBA2-1745622547</TxnLineID>
                            <ItemRef>
                                <ListID>800008EA-1744215679</ListID>
                                <FullName>Duty 145% Customer</FullName>
                            </ItemRef>
                            <Desc>Tariff 145% Additional ($0.18995/pc)</Desc>
                            <Quantity>1</Quantity>
                            <Rate>56985.00</Rate>
                            <Amount>56985.00</Amount>
                            <SalesTaxCodeRef>
                                <ListID>80000002-1693363606</ListID>
                                <FullName>Non</FullName>
                            </SalesTaxCodeRef>
                            <Invoiced>0</Invoiced>
                            <IsManuallyClosed>false</IsManuallyClosed>
                        </SalesOrderLineRet>
                    </SalesOrderRet>
                </SalesOrderQueryRs>
            </QBXMLMsgsRs>
        </QBXML>"""
        root = et.fromstring(LINES_XML)
        sales_order_el = root.find(".//SalesOrderRet")
        sales_order = SalesOrder.from_xml(sales_order_el)

        self.assertEqual(sales_order.txn_id, "1DB9A-1745622547")

        self.assertEqual(len(sales_order.sales_order_lines), 2)

        line1 = sales_order.sales_order_lines[0]
        self.assertEqual(line1.txn_line_id, "1DB9C-1745622547")
        self.assertEqual(line1.desc.strip(),
                         "Pump OLLY BW 28-410 JL-AMA\n\n                        PART #64894547".strip())
        self.assertEqual(line1.quantity, 300000)
        self.assertEqual(line1.rate, Decimal('0.15'))
        self.assertEqual(line1.amount, Decimal("45000.00"))

        line2 = sales_order.sales_order_lines[1]
        self.assertEqual(line2.txn_line_id, "1DBA2-1745622547")
        self.assertEqual(line2.desc.strip(), "Tariff 145% Additional ($0.18995/pc)")
        self.assertEqual(line2.quantity, 1)
        self.assertEqual(line2.rate, 56985.00)
        self.assertEqual(line2.amount, Decimal("56985.00"))

