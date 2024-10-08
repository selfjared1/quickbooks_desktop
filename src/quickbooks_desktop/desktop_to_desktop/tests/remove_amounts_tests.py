
import unittest
from lxml import etree
from src.quickbooks_desktop.desktop_to_desktop.utilities import remove_amount_if_qty_and_rate, remove_amount_from_subtotals

class TestRemoveAmountTags(unittest.TestCase):
    def test_remove_amount_tags(self):
        # Your sample XML content
        xml_content = """<?xml version="1.0" ?>
<QBXML>
<QBXMLMsgsRs>
<TimeTrackingQueryRs requestID="1" statusCode="1" statusSeverity="Info" statusMessage="A query request did not find a matching object in QuickBooks" />
<VehicleMileageQueryRs requestID="2" statusCode="1" statusSeverity="Info" statusMessage="A query request did not find a matching object in QuickBooks" />
<EstimateQueryRs requestID="3" statusCode="0" statusSeverity="Info" statusMessage="Status OK">
<EstimateRet>
<TxnID>DCEEF-1675796632</TxnID>
<!-- ... other elements ... -->
<EstimateLineRet>
    <TxnLineID>DCEF1-1675796632</TxnLineID>
    <ItemRef>
        <ListID>800016D0-1623185743</ListID>
        <FullName>Y1002892</FullName>
    </ItemRef>
    <Desc>NSK Nakanishi&#174; Volvere i7 Dental Lab Grinder - AC 100-240V 50/60Hz  - 1,000 - 35,000rpm</Desc>
    <Quantity>2</Quantity>
    <Rate>891</Rate>
    <Amount>1782.00</Amount>
    <SalesTaxCodeRef>
        <ListID>80000001-1622403872</ListID>
        <FullName>TAX</FullName>
    </SalesTaxCodeRef>
    <DataExtRet>
        <OwnerID>0</OwnerID>
        <DataExtName>Discount Code</DataExtName>
        <DataExtType>STR255TYPE</DataExtType>
        <DataExtValue>N</DataExtValue>
    </DataExtRet>
</EstimateLineRet>
<EstimateLineRet>
    <TxnLineID>DCEF2-1675796632</TxnLineID>
    <ItemRef>
        <ListID>800016F4-1623185781</ListID>
        <FullName>NR-303</FullName>
    </ItemRef>
    <Desc>NSK Nakanishi&#174; 22.8mm &#216; Spindle (-) - 30,000 max.rpm  CHK</Desc>
    <Quantity>2</Quantity>
    <Rate>589.00</Rate>
    <Amount>1178.00</Amount>
    <SalesTaxCodeRef>
        <ListID>80000001-1622403872</ListID>
        <FullName>TAX</FullName>
    </SalesTaxCodeRef>
    <DataExtRet>
        <OwnerID>0</OwnerID>
        <DataExtName>Discount Code</DataExtName>
        <DataExtType>STR255TYPE</DataExtType>
        <DataExtValue>N</DataExtValue>
    </DataExtRet>
</EstimateLineRet>
<!-- Additional EstimateLineRet elements -->
</EstimateRet>
</EstimateQueryRs>
</QBXMLMsgsRs>
</QBXML>
"""

        # Parse the XML content
        root = etree.fromstring(xml_content.encode('utf-8'))

        # Before modification: check that Amount tags exist
        amount_tags_before = root.xpath(".//EstimateLineRet[Quantity and Rate]/Amount")
        self.assertTrue(len(amount_tags_before) > 0, "Amount tags should exist before modification")

        # Call the function to remove Amount tags
        modified_root = remove_amount_if_qty_and_rate(root)

        # After modification: check that Amount tags are removed
        amount_tags_after = modified_root.xpath(".//EstimateLineRet[Quantity and Rate]/Amount")
        self.assertEqual(len(amount_tags_after), 0, "Amount tags should be removed after modification")

        # Additionally, ensure that other Amount tags are not removed if they don't meet the condition
        # For this test, we assume all Amount tags in EstimateLineRet with Quantity and Rate should be removed

        # Optionally, print the modified XML (commented out)
        # output_xml = etree.tostring(modified_root, encoding='utf-8', xml_declaration=True, pretty_print=True).decode('utf-8')
        # print(output_xml)


import unittest
from lxml import etree

# Assume remove_amount_tags_by_item_names is already defined and imported

class TestRemoveAmountTagsByItemNames(unittest.TestCase):

    def test_remove_amount_tags_by_item_names(self):
        # Sample XML content
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
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
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>Y1002892</FullName>
                    </ItemRef>
                    <Desc>NSK Nakanishi Volvere i7 Dental Lab Grinder - AC 100-240V 50/60Hz  - 1,000 - 35,000rpm</Desc>
                    <Quantity>2</Quantity>
                    <Rate>891</Rate>
                    <SalesTaxCodeRef>
                        <FullName>TAX</FullName>
                    </SalesTaxCodeRef>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>Amount Subtotal</FullName>
                    </ItemRef>
                    <Desc>Subtotal</Desc>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>5% Discount</FullName>
                    </ItemRef>
                    <Desc>5% Discount</Desc>
                    <RatePercent>-5.00</RatePercent>
                    <Amount>-89.10</Amount>
                    <SalesTaxCodeRef>
                        <FullName>TAX</FullName>
                    </SalesTaxCodeRef>
                </EstimateLineAdd>
                <EstimateLineAdd>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>NR-303</FullName>
                    </ItemRef>
                    <Desc>NSK Nakanishi 22.8mm O Spindle (-) - 30,000 max.rpm  CHK</Desc>
                    <Quantity>2</Quantity>
                    <Rate>589.00</Rate>
                    <Amount>1178.00</Amount>
                    <SalesTaxCodeRef>
                        <FullName>TAX</FullName>
                    </SalesTaxCodeRef>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>Tool Holding:91593</FullName>
                    </ItemRef>
                    <Desc>NSK Nakanishi CHK Collet - 3.175mm / 1/8"o</Desc>
                    <Quantity>2</Quantity>
                    <Rate>95.00</Rate>
                    <Amount>190.00</Amount>
                    <SalesTaxCodeRef>
                        <FullName>TAX</FullName>
                    </SalesTaxCodeRef>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>Amount Subtotal</FullName>
                    </ItemRef>
                    <Desc>Subtotal</Desc>
                    <Amount>1368.00</Amount>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>15% Discount</FullName>
                    </ItemRef>
                    <Desc>15% Discount</Desc>
                    <RatePercent>-15.00</RatePercent>
                    <Amount>-205.20</Amount>
                    <SalesTaxCodeRef>
                        <FullName>TAX</FullName>
                    </SalesTaxCodeRef>
                </EstimateLineAdd>
                <EstimateLineAdd>
                </EstimateLineAdd>
                <EstimateLineAdd>
                    <ItemRef>
                        <FullName>STerms1</FullName>
                    </ItemRef>
                    <Desc>Terms: Open account; net 30 days.
Availability: From stock, subject to prior sales.
Delivery Terms: EXW, via UPS ground collect, unless otherwise requested.
Validity of Offer: 60 Days.</Desc>
                    <Amount>0.00</Amount>
                    <SalesTaxCodeRef>
                        <FullName>TAX</FullName>
                    </SalesTaxCodeRef>
                </EstimateLineAdd>
            </EstimateAdd>
        </EstimateAddRq>
    </QBXMLMsgsRq>
</QBXML>"""

        # Parse the XML content
        root = etree.fromstring(xml_content.encode('utf-8'))

        # Define item_names to search for
        item_names = ['Y1002892', 'NR-303', 'Tool Holding:91593']

        # Before modification: check that Amount tags exist for specified item_names
        amount_tags_before = root.xpath(
            ".//ItemRef[FullName='Y1002892']/../Amount | "
            ".//ItemRef[FullName='NR-303']/../Amount | "
            ".//ItemRef[FullName='Tool Holding:91593']/../Amount"
        )
        self.assertEqual(len(amount_tags_before), 3, "Amount tags should exist before modification for specified item_names")

        # Call the function to remove Amount tags
        modified_root = remove_amount_from_subtotals(root, item_names)

        # After modification: check that Amount tags are removed for specified item_names
        amount_tags_after = modified_root.xpath(
            ".//ItemRef[FullName='Y1002892']/../Amount | "
            ".//ItemRef[FullName='NR-303']/../Amount | "
            ".//ItemRef[FullName='Tool Holding:91593']/../Amount"
        )
        self.assertEqual(len(amount_tags_after), 0, "Amount tags should be removed after modification for specified item_names")

        # Ensure that Amount tags in non-specified items are not removed
        # For example, '5% Discount' and 'Amount Subtotal' should still have Amount tags
        amount_tags_other = modified_root.xpath(
            ".//ItemRef[FullName!='Y1002892' and FullName!='NR-303' and FullName!='Tool Holding:91593']/../Amount"
        )
        self.assertTrue(len(amount_tags_other) > 0, "Amount tags in non-specified items should remain")

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
