import unittest
from lxml import etree
from src.quickbooks_desktop.desktop_to_desktop.utilities import reorder_xml_in_entire_document

class TestReorderXMLFunction(unittest.TestCase):

    def test_reorder_exchange_rate(self):
        # Provided XML content
        xml_content = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
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
                        <ExchangeRate>1</ExchangeRate>
                        <IsToBeEmailed>false</IsToBeEmailed>
                        <CustomerSalesTaxCodeRef>
                            <FullName>TAX</FullName>
                        </CustomerSalesTaxCodeRef>
                        <EstimateLineAdd>
                            <ItemRef>
                                <FullName>Y1002892</FullName>
                            </ItemRef>
                            <Desc>NSK Nakanishi Volvere i7 Dental Lab Grinder - AC 100-240V 50/60Hz  - 1,000 - 35,000rpm</Desc>
                            <Quantity>2</Quantity>
                            <Rate>891</Rate>
                            <Amount>1782.00</Amount>
                            <SalesTaxCodeRef>
                                <FullName>TAX</FullName>
                            </SalesTaxCodeRef>
                        </EstimateLineAdd>
                        <!-- Additional EstimateLineAdd elements -->
                    </EstimateAdd>
                </EstimateAddRq>
            </QBXMLMsgsRq>
        </QBXML>"""

        # Parse the XML content
        root = etree.fromstring(xml_content.encode('utf-8'))

        # Parameters for reordering
        parent_to_loop_through = "EstimateAddRq"
        out_of_place_tag = "ExchangeRate"
        tag_before = "ItemSalesTaxRef"
        tag_after = "EstimateLineAdd"

        # Assume the function reorder_xml_in_entire_document is already defined and imported
        # Call the function to reorder the XML
        reorder_xml_in_entire_document(
            entire_xml=root,
            parent_to_loop_through=parent_to_loop_through,
            out_of_place_tag=out_of_place_tag,
            tag_before=tag_before,
            tag_after=tag_after
        )

        # Find the EstimateAdd element
        estimate_add_rq = root.find('.//EstimateAddRq')
        estimate_add = estimate_add_rq.find('EstimateAdd')

        # Get the list of child tags in EstimateAdd
        child_tags = [child.tag for child in estimate_add]

        # Find the positions of the relevant tags
        try:
            item_sales_tax_ref_index = child_tags.index('ItemSalesTaxRef')
        except ValueError:
            item_sales_tax_ref_index = -1  # Tag not found

        try:
            exchange_rate_index = child_tags.index('ExchangeRate')
        except ValueError:
            exchange_rate_index = -1  # Tag not found

        # Assert that ExchangeRate comes after ItemSalesTaxRef
        self.assertNotEqual(exchange_rate_index, -1, "ExchangeRate tag not found")
        self.assertNotEqual(item_sales_tax_ref_index, -1, "ItemSalesTaxRef tag not found")
        self.assertEqual(exchange_rate_index, item_sales_tax_ref_index + 1, "ExchangeRate tag is not immediately after ItemSalesTaxRef tag")

        # Optionally, you can print the child tags for debugging
        # print("Child tags in EstimateAdd after reordering:", child_tags)
