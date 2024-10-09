import unittest
import xml.etree.ElementTree as ET
from src.quickbooks_desktop.desktop_to_desktop.utilities import reorder_specific_tag_in_document


class TestReorderSpecificTagInDocument(unittest.TestCase):

    def setUp(self):
        # XML string provided in the question
        self.xml_str = '''<?xml version="1.0" encoding="utf-8"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                <EstimateAddRq requestID="1">
                    <EstimateAdd>
                        <CustomerRef>
                            <FullName>FKN Systek Inc. (C)</FullName>
                        </CustomerRef>
                        <TemplateRef>
                            <FullName>ARTCO Quote2</FullName>
                        </TemplateRef>
                        <TxnDate>2003-11-01</TxnDate>
                        <RefNumber>Q23-0147-1</RefNumber>
                        <BillAddress>
                            <Addr1>FKN Systek Inc.</Addr1>
                            <Addr2>115  Pleasant Street</Addr2>
                            <City>Millis</City>
                            <State>MA</State>
                            <PostalCode>02054</PostalCode>
                        </BillAddress>
                        <ShipAddress>
                            <Addr1>FKN SYSTEK</Addr1>
                            <Addr2>115  PLEASANT ST</Addr2>
                            <City>MILLS</City>
                            <State>MA</State>
                            <PostalCode>02054</PostalCode>
                        </ShipAddress>
                        <IsActive>true</IsActive>
                        <PONumber>Pending</PONumber>
                        <TermsRef>
                            <FullName>Net 30 Days</FullName>
                        </TermsRef>
                        <DueDate>2003-12-01</DueDate>
                        <ItemSalesTaxRef>
                            <FullName>AVATAX</FullName>
                        </ItemSalesTaxRef>
                        <IsToBeEmailed>false</IsToBeEmailed>
                        <CustomerSalesTaxCodeRef>
                            <FullName>TAX</FullName>
                        </CustomerSalesTaxCodeRef>
                        <ExchangeRate>1</ExchangeRate>
                    </EstimateAdd>
                </EstimateAddRq>
            </QBXMLMsgsRq>
        </QBXML>'''

        # Parse XML into ElementTree structure
        self.qbxml_msgs = ET.ElementTree(ET.fromstring(self.xml_str))

        # Order of tags we want
        self.tag_order_list = ['ItemSalesTaxRef', 'Memo', 'CustomerMsgRef', 'IsToBeEmailed', 'CustomerSalesTaxCodeRef',
                               'Other', 'ExchangeRate']

    def test_reorder_specific_tag_in_document(self):
        # Call the function to reorder
        reorder_specific_tag_in_document(self.qbxml_msgs.getroot(), './/EstimateAdd', self.tag_order_list,
                                         'ExchangeRate')

        # After reordering, we expect ExchangeRate to be placed after CustomerSalesTaxCodeRef
        estimate_add = self.qbxml_msgs.find('.//EstimateAdd')

        # Retrieve the tag order after reordering
        reordered_tags = [child.tag for child in estimate_add]

        # Assert that 'ExchangeRate' comes after 'CustomerSalesTaxCodeRef'
        self.assertGreater(reordered_tags.index('ExchangeRate'), reordered_tags.index('CustomerSalesTaxCodeRef'))

        # Assert that the other tags still exist in the correct order as per the tag_order_list
        expected_order = [tag for tag in self.tag_order_list if tag in reordered_tags]
        self.assertEqual(expected_order, reordered_tags[-len(expected_order):])  # Check if reordered tags match
        # print(ET.tostring(self.qbxml_msgs))


