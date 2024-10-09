import unittest
from lxml import etree
from src.quickbooks_desktop.desktop_to_desktop.utilities import reorder_specific_tag_in_document, remove_unwanted_tags

class TestReorderXMLFunction(unittest.TestCase):

    def test_reorder_exchange_rate_sales_order(self):
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

        tag_order_list = ['ItemSalesTaxRef', 'Memo', 'CustomerMsgRef', 'IsToBeEmailed', 'CustomerSalesTaxCodeRef',
                          'Other',
                          'ExchangeRate', 'ExternalGUID']

        reorder_specific_tag_in_document(root, 'EstimateAdd', tag_order_list, 'ExchangeRate')


        # Find the EstimateAdd element
        estimate_add_rq = root.find('.//EstimateAddRq')
        estimate_add = estimate_add_rq.find('EstimateAdd')

        # Get the list of child tags in EstimateAdd
        child_tags = [child.tag for child in estimate_add]

        customer_sales_tax_Code_ref_index = child_tags.index('CustomerSalesTaxCodeRef')

        next_tag = child_tags[customer_sales_tax_Code_ref_index + 1]

        self.assertEqual(next_tag, 'ExchangeRate')

    def test_reorder_exchange_rate_purchase_order(self):
        # Provided XML content
        xml_content = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                <PurchaseOrderAddRq>
                <PurchaseOrderAdd>
                <VendorRef>
                    <FullName>B-B Chemical Corp.</FullName>
                    </VendorRef>
                    <ClassRef>
                    <FullName>Wholesale</FullName>
                    </ClassRef>
                    <TemplateRef>
                    <FullName>ARTCO Drop Ship Purchase Order</FullName>
                    </TemplateRef>
                    <TxnDate>2021-02-08</TxnDate>
                    <RefNumber>64311</RefNumber>
                    <VendorAddress>
                    <Addr1>B-B CHEMICAL CORPORATION</Addr1>
                    <Addr2>2816  CENTRE CIRCLE</Addr2>
                    <City>DOWNERS GROVE</City>
                    <State>IL</State>
                    <PostalCode>60515</PostalCode>
                    </VendorAddress>
                    <ShipAddress>
                    <Addr1>American Rotary Tools Co.</Addr1>
                    <Addr2>250 West Duarte Rd., Suite E</Addr2>
                    <City>Monroiva</City>
                    <State>CA</State>
                    <Country>USA</Country>
                    </ShipAddress>
                    <TermsRef>
                    <FullName>Net 30 Days</FullName>
                    </TermsRef>
                    <DueDate>2021-03-10</DueDate>
                    <ExpectedDate>2021-11-26</ExpectedDate>
                    <ExchangeRate>1</ExchangeRate>
                    <IsToBePrinted>false</IsToBePrinted>
                    <IsToBeEmailed>false</IsToBeEmailed>
                    <Other2>Debra Frank</Other2>
                    <PurchaseOrderLineAdd>
                    <ItemRef>
                    <FullName>Layout Fluids:C2243BL1</FullName>
                    </ItemRef>
                    <ManufacturerPartNumber>KB3V6901</ManufacturerPartNumber>
                    <Desc>Canode Blue Die Spotting Ink - 1 Gallon</Desc>
                    <Quantity>30</Quantity>
                    <Rate>75.00</Rate>
                    <ClassRef>
                    <FullName>Wholesale</FullName>
                    </ClassRef>
                    <Amount>2250.00</Amount>
                    <IsManuallyClosed>true</IsManuallyClosed>
                    </PurchaseOrderLineAdd>
                    </PurchaseOrderAdd>
                  </PurchaseOrderAddRq>
            </QBXMLMsgsRq>
        </QBXML>"""

        # Parse the XML content
        root = etree.fromstring(xml_content.encode('utf-8'))

        po_tag_order_list = ['DueDate', 'ExpectedDate', 'ShipMethodRef', 'FOB', 'Memo', 'VendorMsg', 'IsToBePrinted',
                             'IsToBeEmailed', 'Other1', 'Other2', 'ExchangeRate', 'ExternalGUID']
        reorder_specific_tag_in_document(root, 'PurchaseOrderAdd', po_tag_order_list, 'ExchangeRate')


        # Find the EstimateAdd element
        purchase_order_add_rq = root.find('.//PurchaseOrderAddRq')
        purchase_order_add = purchase_order_add_rq.find('PurchaseOrderAdd')

        # Get the list of child tags in EstimateAdd
        child_tags = [child.tag for child in purchase_order_add]

        other_2_index = child_tags.index('Other2')

        next_tag = child_tags[other_2_index + 1]

        self.assertEqual(next_tag, 'ExchangeRate')

    def test_remove_tag_purchase_order(self):
        # Provided XML content
        xml_content = """<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                <PurchaseOrderAddRq>
                    <PurchaseOrderAdd>
                        <VendorRef>
                        <FullName>B-B Chemical Corp.</FullName>
                        </VendorRef>
                        <ClassRef>
                        <FullName>Wholesale</FullName>
                        </ClassRef>
                        <TemplateRef>
                        <FullName>ARTCO Drop Ship Purchase Order</FullName>
                        </TemplateRef>
                        <TxnDate>2021-02-08</TxnDate>
                        <RefNumber>64311</RefNumber>
                        <VendorAddress>
                        <Addr1>B-B CHEMICAL CORPORATION</Addr1>
                        <Addr2>2816  CENTRE CIRCLE</Addr2>
                        <City>DOWNERS GROVE</City>
                        <State>IL</State>
                        <PostalCode>60515</PostalCode>
                        </VendorAddress>
                        <ShipAddress>
                        <Addr1>American Rotary Tools Co.</Addr1>
                        <Addr2>250 West Duarte Rd., Suite E</Addr2>
                        <City>Monroiva</City>
                        <State>CA</State>
                        <Country>USA</Country>
                        </ShipAddress>
                        <TermsRef>
                        <FullName>Net 30 Days</FullName>
                        </TermsRef>
                        <DueDate>2021-03-10</DueDate>
                        <ExpectedDate>2021-11-26</ExpectedDate>
                        <ExchangeRate>1</ExchangeRate>
                        <IsToBePrinted>false</IsToBePrinted>
                        <IsToBeEmailed>false</IsToBeEmailed>
                        <Other2>Debra Frank</Other2>
                        <PurchaseOrderLineAdd>
                        <ItemRef>
                        <FullName>Layout Fluids:C2243BL1</FullName>
                        </ItemRef>
                        <ManufacturerPartNumber>KB3V6901</ManufacturerPartNumber>
                        <Desc>Canode Blue Die Spotting Ink - 1 Gallon</Desc>
                        <Quantity>30</Quantity>
                        <Rate>75.00</Rate>
                        <ClassRef>
                        <FullName>Wholesale</FullName>
                        </ClassRef>
                        <Amount>2250.00</Amount>
                        <IsManuallyClosed>true</IsManuallyClosed>
                        </PurchaseOrderLineAdd>
                    </PurchaseOrderAdd>
                  </PurchaseOrderAddRq>
            </QBXMLMsgsRq>
        </QBXML>"""

        root = etree.fromstring(xml_content.encode('utf-8'))

        general_tags_to_remove = ['PurchaseOrderRet/PurchaseOrderLineRet/IsManuallyClosed']

        root = remove_unwanted_tags(root, general_tags_to_remove)

        existing_matching_tags = root.xpath('//IsManuallyClosed')
        self.assertEqual(len(existing_matching_tags), 0)