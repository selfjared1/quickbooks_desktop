import unittest
from unittest.mock import patch, MagicMock
from lxml import etree as et
from decimal import Decimal
from datetime import datetime
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop, Estimate, EstimateLine, QBDateTime

class TestCreateEstimate(unittest.TestCase):

    def setUp(self):
        self.estimate_xml = """
        <EstimateRet>
            <TxnID>DCEEF-1675796632</TxnID>
            <TimeCreated>2023-02-07T12:03:52-07:00</TimeCreated>
            <TimeModified>2024-01-08T18:34:18-07:00</TimeModified>
            <EditSequence>1698868818</EditSequence>
            <TxnNumber>104125</TxnNumber>
            <CustomerRef>
            <ListID>80004587-1623722347</ListID>
            <FullName>FKN Systek Inc. (C)</FullName>
            </CustomerRef>
            <TemplateRef>
            <ListID>80000047-1644348521</ListID>
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
            <BillAddressBlock>
            <Addr1>FKN Systek Inc.</Addr1>
            <Addr2>115  Pleasant Street</Addr2>
            <Addr3>Millis, MA  02054</Addr3>
            </BillAddressBlock>
            <ShipAddress>
            <Addr1>FKN SYSTEK</Addr1>
            <Addr2>115  PLEASANT ST</Addr2>
            <City>MILLS</City>
            <State>MA</State>
            <PostalCode>02054</PostalCode>
            </ShipAddress>
            <ShipAddressBlock>
            <Addr1>FKN SYSTEK</Addr1>
            <Addr2>115  PLEASANT ST</Addr2>
            <Addr3>MILLS, MA  02054</Addr3>
            </ShipAddressBlock>
            <IsActive>true</IsActive>
            <PONumber>Pending</PONumber>
            <TermsRef>
            <ListID>80000006-1622403879</ListID>
            <FullName>Net 30 Days</FullName>
            </TermsRef>
            <DueDate>2003-12-01</DueDate>
            <Subtotal>2855.70</Subtotal>
            <ItemSalesTaxRef>
            <ListID>80006E8A-1642522937</ListID>
            <FullName>AVATAX</FullName>
            </ItemSalesTaxRef>
            <SalesTaxPercentage>0.00</SalesTaxPercentage>
            <SalesTaxTotal>0.00</SalesTaxTotal>
            <TotalAmount>2855.70</TotalAmount>
            <CurrencyRef>
            <ListID>80000096-1622403877</ListID>
            <FullName>US Dollar</FullName>
            </CurrencyRef>
            <ExchangeRate>1</ExchangeRate>
            <TotalAmountInHomeCurrency>2855.70</TotalAmountInHomeCurrency>
            <IsToBeEmailed>false</IsToBeEmailed>
            <CustomerSalesTaxCodeRef>
            <ListID>80000001-1622403872</ListID>
            <FullName>TAX</FullName>
            </CustomerSalesTaxCodeRef>
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
            <TxnLineID>DE02C-1675796632</TxnLineID>
            <ItemRef>
            <ListID>80002EAA-1628095182</ListID>
            <FullName>Amount Subtotal</FullName>
            </ItemRef>
            <Desc>Subtotal</Desc>
            <Amount>1782.00</Amount>
            </EstimateLineRet>
            <EstimateLineRet>
            <TxnLineID>DDFC1-1675796632</TxnLineID>
            <ItemRef>
            <ListID>80002EA8-1628031674</ListID>
            <FullName>5% Discount</FullName>
            </ItemRef>
            <Desc>5% Discount</Desc>
            <RatePercent>-5.00</RatePercent>
            <Amount>-89.10</Amount>
            <SalesTaxCodeRef>
            <ListID>80000001-1622403872</ListID>
            <FullName>TAX</FullName>
            </SalesTaxCodeRef>
            </EstimateLineRet>
            <EstimateLineRet>
            <TxnLineID>DDFC2-1675796632</TxnLineID>
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
            <EstimateLineRet>
            <TxnLineID>DCEF3-1675796632</TxnLineID>
            <ItemRef>
            <ListID>8000289C-1623253956</ListID>
            <FullName>Tool Holding:91593</FullName>
            </ItemRef>
            <Desc>NSK Nakanishi&#174; CHK Collet - 3.175mm / 1/8&quot;&#248;</Desc>
            <Quantity>2</Quantity>
            <Rate>95.00</Rate>
            <Amount>190.00</Amount>
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
            <TxnLineID>DCEF4-1675796632</TxnLineID>
            <ItemRef>
            <ListID>80002EAA-1628095182</ListID>
            <FullName>Amount Subtotal</FullName>
            </ItemRef>
            <Desc>Subtotal</Desc>
            <Amount>1368.00</Amount>
            </EstimateLineRet>
            <EstimateLineRet>
            <TxnLineID>DCEF5-1675796632</TxnLineID>
            <ItemRef>
            <ListID>80002EA5-1628013426</ListID>
            <FullName>15% Discount</FullName>
            </ItemRef>
            <Desc>15% Discount</Desc>
            <RatePercent>-15.00</RatePercent>
            <Amount>-205.20</Amount>
            <SalesTaxCodeRef>
            <ListID>80000001-1622403872</ListID>
            <FullName>TAX</FullName>
            </SalesTaxCodeRef>
            </EstimateLineRet>
            <EstimateLineRet>
            <TxnLineID>DCEF6-1675796632</TxnLineID>
            </EstimateLineRet>
            <EstimateLineRet>
            <TxnLineID>DCEF7-1675796632</TxnLineID>
            <ItemRef>
            <ListID>80006E83-1642029028</ListID>
            <FullName>STerms1</FullName>
            </ItemRef>
            <Desc>Terms: Open account; net 30 days.
            Availability: From stock, subject to prior sales.
            Delivery Terms: EXW, via UPS ground collect, unless otherwise requested.
            Validity of Offer: 60 Days.</Desc>
            <Amount>0.00</Amount>
            <SalesTaxCodeRef>
            <ListID>80000001-1622403872</ListID>
            <FullName>TAX</FullName>
            </SalesTaxCodeRef>
            </EstimateLineRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Customer Type</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Dealer</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>As Of</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>01-25-13</DataExtValue>
            </DataExtRet>
            <DataExtRet>
            <OwnerID>0</OwnerID>
                <DataExtName>UHL Account No.</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>12248</DataExtValue>
            </DataExtRet>
            <DataExtRet>
            <OwnerID>0</OwnerID>
                <DataExtName>AKA / DBA</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>SYSTECH SKN NSK IEC</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Division</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>New England</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Region</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Northeast</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Vendor</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>UPS</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Method</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Collect</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Account</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>69A74F</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Contact</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Werner Christ</DataExtValue>
            </DataExtRet>
            </EstimateRet>
        """

        self.estimate_just_data_ext_xml = """
                <EstimateRet>
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
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Customer Type</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>Dealer</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>As Of</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>01-25-13</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>UHL Account No.</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>12248</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>AKA / DBA</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>SYSTECH SKN NSK IEC</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Division</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>New England</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Region</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>Northeast</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Ship Vendor</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>UPS</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Ship Method</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>Collect</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Ship Account</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>69A74F</DataExtValue>
                </DataExtRet>
                <DataExtRet>
                    <OwnerID>0</OwnerID>
                    <DataExtName>Contact</DataExtName>
                    <DataExtType>STR255TYPE</DataExtType>
                    <DataExtValue>Werner Christ</DataExtValue>
                </DataExtRet>
                </EstimateRet>
                """

    def test_create_estimate_just_data_ext(self):
        estimate = Estimate.from_xml(self.estimate_just_data_ext_xml)
        # DataExtRet checks
        self.assertEqual(len(estimate.data_ext), 10)
        self.assertEqual(estimate.data_ext[0].data_ext_name, 'Customer Type')
        self.assertEqual(estimate.data_ext[0].data_ext_value, 'Dealer')
        self.assertEqual(estimate.data_ext[1].data_ext_name, 'As Of')
        self.assertEqual(estimate.data_ext[1].data_ext_value, '01-25-13')
        self.assertEqual(estimate.data_ext[2].data_ext_name, 'UHL Account No.')
        self.assertEqual(estimate.data_ext[2].data_ext_value, '12248')
        self.assertEqual(estimate.data_ext[3].data_ext_name, 'AKA / DBA')
        self.assertEqual(estimate.data_ext[3].data_ext_value, 'SYSTECH SKN NSK IEC')
        self.assertEqual(len(estimate.estimate_lines[0].data_ext), 1)


    def test_create_estimate(self):
        estimate = Estimate.from_xml(self.estimate_xml)

        # Basic attribute checks
        self.assertEqual(estimate.txn_id, 'DCEEF-1675796632')
        self.assertEqual(estimate.time_created, QBDateTime('2023-02-07T12:03:52-07:00'))
        self.assertEqual(estimate.time_modified, QBDateTime('2024-01-08T18:34:18-07:00'))
        self.assertEqual(estimate.edit_sequence, '1698868818')
        self.assertEqual(estimate.txn_number, '104125')
        self.assertEqual(estimate.is_active, True)
        self.assertEqual(estimate.ponumber, 'Pending')
        self.assertEqual(estimate.subtotal, Decimal('2855.70'))
        self.assertEqual(estimate.sales_tax_percentage, 0.00)
        self.assertEqual(estimate.sales_tax_total, Decimal('0.00'))
        self.assertEqual(estimate.total_amount, Decimal('2855.70'))
        self.assertEqual(estimate.exchange_rate, 1.0)
        self.assertEqual(estimate.total_amount_in_home_currency, Decimal('2855.70'))
        self.assertEqual(estimate.is_to_be_emailed, False)

        # Nested CustomerRef
        self.assertIsNotNone(estimate.customer_ref)
        self.assertEqual(estimate.customer_ref.list_id, '80004587-1623722347')
        self.assertEqual(estimate.customer_ref.full_name, 'FKN Systek Inc. (C)')

        # Nested TemplateRef
        self.assertIsNotNone(estimate.template_ref)
        self.assertEqual(estimate.template_ref.list_id, '80000047-1644348521')
        self.assertEqual(estimate.template_ref.full_name, 'ARTCO Quote2')

        # DataExtRet checks
        self.assertEqual(len(estimate.data_ext), 10)
        self.assertEqual(estimate.data_ext[0].data_ext_name, 'Customer Type')
        self.assertEqual(estimate.data_ext[0].data_ext_value, 'Dealer')
        self.assertEqual(estimate.data_ext[1].data_ext_name, 'As Of')
        self.assertEqual(estimate.data_ext[1].data_ext_value, '01-25-13')
        self.assertEqual(estimate.data_ext[2].data_ext_name, 'UHL Account No.')
        self.assertEqual(estimate.data_ext[2].data_ext_value, '12248')
        self.assertEqual(estimate.data_ext[3].data_ext_name, 'AKA / DBA')
        self.assertEqual(estimate.data_ext[3].data_ext_value, 'SYSTECH SKN NSK IEC')
        self.assertEqual(len(estimate.estimate_lines[0].data_ext), 1)

        # Check EstimateLineRet and DataExt within it
        self.assertEqual(len(estimate.estimate_lines), 10)
        self.assertEqual(estimate.estimate_lines[0].txn_line_id, 'DCEF1-1675796632')
        self.assertEqual(estimate.estimate_lines[0].item_ref.list_id, '800016D0-1623185743')
        self.assertEqual(estimate.estimate_lines[0].item_ref.full_name, 'Y1002892')
        self.assertEqual(estimate.estimate_lines[0].quantity, 2)
        self.assertEqual(estimate.estimate_lines[0].rate, Decimal('891'))
        self.assertEqual(estimate.estimate_lines[0].amount, Decimal('1782.00'))
        self.assertEqual(estimate.estimate_lines[0].data_ext[0].data_ext_name, 'Discount Code')
        self.assertEqual(estimate.estimate_lines[0].data_ext[0].data_ext_value, 'N')
