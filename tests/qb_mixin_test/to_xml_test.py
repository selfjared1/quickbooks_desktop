import unittest
from decimal import Decimal
from src.quickbooks_desktop.quickbooks_desktop import (
    ToXmlMixin, LinkedTxn, QBDates, JournalEntryAdd,
    CurrencyRef, JournalDebitLine, JournalLineMod, AccountRef, JournalCreditLine, JournalEntries, QBDates,
    EstimateLineAdd, ItemRef, SalesTaxCodeRef, ItemInventoryAdd, InvoiceAdd, CustomerRef, InvoiceLineAdd,
    UnitOfMeasureSetRef, IncomeAccountRef, PrefVendorRef, AssetAccountRef
)
from lxml import etree as et
import datetime
from dataclasses import field, dataclass
from typing import Optional, List


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
        data = TestData(name="TestName", is_active=True, description="A description")
        xml_element = data.to_xml()

        # Assert root element
        self.assertEqual(xml_element.tag, "TestData")

        # Assert child elements
        self.assertEqual(xml_element.find("Name").text, "TestName")
        self.assertEqual(xml_element.find("IsActive").text, "true")
        self.assertEqual(xml_element.find("Description").text, "A description")

    def test_to_xml_with_no_field_order(self):
        data = TestData(name="TestName", is_active=False, description=None)
        if hasattr(data, 'FIELD_ORDER'):
            delattr(type(data), 'FIELD_ORDER')
        else:
            pass

        xml_element = data.to_xml()

        # Test order based on field definition when FIELD_ORDER is not present
        elements = list(xml_element)
        self.assertEqual(elements[0].tag, "Name")
        self.assertEqual(elements[1].tag, "IsActive")
        self.assertEqual(len(elements), 2)

    def test_to_xml_with_field_order(self):
        # Add FIELD_ORDER to the dataclass
        TestData.FIELD_ORDER = ["IsActive", "Name", "Description"]
        data = TestData(name="TestName", is_active=True, description="Test description")
        xml_element = data.to_xml()

        # Test order based on FIELD_ORDER
        elements = list(xml_element)
        self.assertEqual(elements[0].tag, "IsActive")
        self.assertEqual(elements[1].tag, "Name")
        self.assertEqual(elements[2].tag, "Description")

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

    def test_to_xml_invoice_add(self):
        invoice_add = InvoiceAdd(
            customer_ref=CustomerRef(list_id='80000001-1326159291', full_name='Netelco, Incorporated'),
            invoice_line_add=[
                InvoiceLineAdd(item_ref=ItemRef(list_id='80000001-1326159384', full_name='Estimating'),
                               desc='Washington ES Low Voltage/Fire Alarm Bid', quantity=Decimal('1'),
                               unit_of_measure=None, rate=Decimal('100.00'), rate_percent=None,
                               price_level_ref=None, class_ref=None, amount=Decimal('100.00'),
                               tax_amount=None, option_for_price_rule_conflict=None,
                               inventory_site_ref=None, inventory_site_location_ref=None, serial_number=None,
                               lot_number=None, service_date=None,
                               sales_tax_code_ref=SalesTaxCodeRef(list_id='80000002-1326158429', full_name='Non'),
                               is_taxable=None, override_item_account_ref=None, other1=None, other2=None,
                               link_to_txn=None),
                InvoiceLineAdd(item_ref=ItemRef(list_id='80000001-1326159385', full_name='Estimating'),
                               desc='Washington ES Low Voltage/Fire Alarm Bid', quantity=Decimal('1'),
                               unit_of_measure=None, rate=Decimal('200.00'), rate_percent=None,
                               price_level_ref=None, class_ref=None, amount=Decimal('100.00'),
                               tax_amount=None, option_for_price_rule_conflict=None,
                               inventory_site_ref=None, inventory_site_location_ref=None, serial_number=None,
                               lot_number=None, service_date=None,
                               sales_tax_code_ref=SalesTaxCodeRef(list_id='80000002-1326158429', full_name='Non'),
                               is_taxable=None, override_item_account_ref=None, other1=None, other2=None,
                               link_to_txn=None)
            ],
            invoice_line_group_add=[])

        xml_element = invoice_add.to_xml()
        self.assertEqual(xml_element.tag, "InvoiceAdd")
        self.assertEqual(xml_element.find("CustomerRef/ListID").text, "80000001-1326159291")
        invoice_line_add_elm = xml_element.findall('InvoiceLineAdd')
        self.assertEqual(len(invoice_line_add_elm), 2)


class TestToXmlMixin2(unittest.TestCase):

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
                txn_date=QBDates(date=datetime.datetime(2023, 8, 25, 0, 0)),
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
        self.assertEqual(element[0].tag, 'LinkedTxn')
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

    def test_inventory_field_order(self):
        item_inventory_add = ItemInventoryAdd(name='050008X', bar_code=None, is_active=True, external_guid=None,
                                          class_ref=None,
                                          sales_tax_code_ref=SalesTaxCodeRef(list_id=None, full_name='TAX'),
                                          parent_ref=None, manufacturer_part_number='0500008X',
                                          unit_of_measure_set_ref=UnitOfMeasureSetRef(list_id=None,
                                                                                      full_name='Count in Each'),
                                          is_tax_included=None,
                                          sales_desc='Single Lip Cutter Grinding Machine S0 (inch)\\nwith grinding spindle, holding fixtue embedded on both sides, dressing unit integratd in protective hood and dust guard for connecting a dust exhaust unit. RAL-9016 - Traffic White\\nWithout Motor\\nWithout Power Plug\\nIncludes Accessories: Wheel Mount and Clamping nut, Cup Grinding Wheel, Set of Wrenches, Operators manual. Plywood with external boarding incl IPPC Certificate.',
                                          sales_price=Decimal('12940.00'),
                                          income_account_ref=IncomeAccountRef(list_id=None, full_name='Sales'),
                                          purchase_desc='Single Lip Cutter Grinding Machine S0 (inch)\\nwith grinding spindle, holding fixtue embedded on both sides, dressing unit integratd in protective hood and dust guard for connecting a dust exhaust unit. RAL-9016 - Traffic White\\nWithout Motor\\nWithout Power Plug\\nIncludes Accessories: Wheel Mount and Clamping nut, Cup Grinding Wheel, Set of Wrenches, Operators manual. Plywood with external boarding incl IPPC Certificate.',
                                          purchase_cost=Decimal('6960.50'), purchase_tax_code_ref=None,
                                          cogsaccount_ref=None,
                                          pref_vendor_ref=PrefVendorRef(list_id=None, full_name='AKS GmbH'),
                                          asset_account_ref=AssetAccountRef(list_id=None, full_name='Inventory Asset'),
                                          max=None, quantity_on_hand=0.0, total_value=None, inventory_date=None,
                                          reorder_point=None)

        item_inventory_xml = item_inventory_add.to_xml()

        actual_tags = [child.tag for child in item_inventory_xml]

        expected_tags = [
        "Name", "IsActive", "ManufacturerPartNumber", "UnitOfMeasureSetRef", "SalesTaxCodeRef",
        "SalesDesc", "SalesPrice", "IncomeAccountRef", "PurchaseDesc",
        "PurchaseCost", "PrefVendorRef", "AssetAccountRef",
        "QuantityOnHand"
    ]
        self.assertEqual(actual_tags, expected_tags, "The XML field order is incorrect.")

    def test_get_sorted_fields(self):
        journal_add = JournalEntryAdd(
            txn_date=QBDates(date=datetime.datetime(2005, 10, 18, 0, 0)),
            ref_number='1',
            memo=None,
            is_adjustment=False,
            is_amounts_entered_in_home_currency=False,
            currency_ref=CurrencyRef(list_id=None, full_name='US Dollar'),
            exchange_rate=1.0, external_guid=None,
            journal_debit_lines=[
                JournalDebitLine(txn_line_id=None,
                                 account_ref=AccountRef(list_id=None, full_name='Automobiles'),
                                 amount=Decimal('4500.00'),
                                 tax_amount=None, memo='original purchase', entity_ref=None,
                                 class_ref=None, item_sales_tax_ref=None, billable_status=None, def_macro=None),
                JournalDebitLine(txn_line_id=None,
                                 account_ref=AccountRef(list_id=None, full_name='Furniture and Fixtures'),
                                 amount=Decimal('2000.00'), tax_amount=None, memo='original purchase',
                                 entity_ref=None, class_ref=None, item_sales_tax_ref=None,
                                 billable_status=None, def_macro=None),
                JournalDebitLine(txn_line_id=None, account_ref=AccountRef(list_id=None, full_name='Inventory'),
                                 amount=Decimal('203500.00'), tax_amount=None, memo='original purchase',
                                 entity_ref=None, class_ref=None, item_sales_tax_ref=None,
                                 billable_status=None, def_macro=None)
            ],
            journal_credit_lines=[
                JournalCreditLine(txn_line_id=None, account_ref=AccountRef(list_id=None, full_name='Notes - Artco, Inc.'),
                                  amount=Decimal('210000.00'), tax_amount=None, memo='original purchase',
                                  entity_ref=None, class_ref=None, item_sales_tax_ref=None,
                                  billable_status=None, def_macro=None)
            ])

        j_xml = journal_add.to_xml()
        #todo: make tests

    def test__create_xml_element(self):
        root = et.fromstring('<EstimateLineAdd><ItemRef><FullName>DA3H218</FullName></ItemRef></EstimateLineAdd>')
        desc = field(
        default=None,
        metadata={
            "name": "Desc",
            "type": "Element",
            "max_length": 4095,
        },
        )
        value = """ARTCO 11A2 Diamond Grinding Wheel - 3.5&quot; &#216; &#215; 1.3&quot; &#215; 20mm Hole - D220, N100, B1/8&quot;, W3/8&quot;"""
        estimate_line_add = EstimateLineAdd(
            item_ref=ItemRef(list_id=None, full_name='DA3H218'),
            desc="""ARTCO 11A2 Diamond Grinding Wheel - 3.5&quot; &#216; &#215; 1.3&quot; &#215; 20mm Hole - D220, N100, B1/8&quot;, W3/8&quot;""",
            quantity=1.0,
            unit_of_measure='each',
            rate=None,
            rate_percent=None,
            class_ref=None,
            amount=Decimal(225.00), tax_amount=None,
            option_for_price_rule_conflict=None, inventory_site_ref=None, inventory_site_location_ref=None,
            sales_tax_code_ref=SalesTaxCodeRef(list_id=None, full_name='TAX'),
            markup_rate=None, markup_rate_percent=None, price_level_ref=None, override_item_account_ref=None, other1=None, other2=None)
        element = estimate_line_add._create_xml_element(root, desc, value)
        desc_str = et.tostring(element, pretty_print=True).decode("ISO-8859-1")
        self.assertFalse('&amp;amp;' in desc_str, "Over-escaping detected in desc_str")
        self.assertIn('&amp;', desc_str, "Ampersand is not escaped correctly as '&amp;'")
