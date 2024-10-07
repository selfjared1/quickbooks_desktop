import unittest
import lxml.etree as ET
from src.quickbooks_desktop.desktop_to_desktop.utilities import add_data_ext_add, transform_qbxml

class TestAddDataExtAdd(unittest.TestCase):

    def setUp(self):
        self.data_ext_rets = '''
        <root>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Method</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Overnight</DataExtValue>
            </DataExtRet>
            <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Vendor</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Fed Ex</DataExtValue>
            </DataExtRet>
        </root>
        '''
        self.data_ext_rets_root = ET.fromstring(self.data_ext_rets)
        self.new_qbxml_msgs = ET.Element("QBXMLMsgsRq", onError="stopOnError")

    def test_add_data_ext_add_with_list_id(self):
        parent_id_macro = "ListID:12345"
        data_ext_rets = self.data_ext_rets_root.findall(".//DataExtRet")
        request_counter = 1
        created_count, new_request_counter = add_data_ext_add(self.new_qbxml_msgs, data_ext_rets, parent_id_macro, request_counter)
        self.assertEqual(created_count, 2)
        self.assertEqual(new_request_counter, 3)
        data_ext_add_rqs = self.new_qbxml_msgs.findall(".//DataExtAddRq")
        self.assertEqual(len(data_ext_add_rqs), 2)
        self.assertEqual(data_ext_add_rqs[0].attrib['requestID'], '1')
        list_data_ext_type = data_ext_add_rqs[0].find(".//ListDataExtType")
        self.assertEqual(list_data_ext_type.text, "Customer")
        list_id = data_ext_add_rqs[0].find(".//ListObjRef/ListID")
        self.assertEqual(list_id.attrib['useMacro'], "ListID:12345")

    def test_add_data_ext_add_with_txn_id(self):
        parent_id_macro = "TxnID:98765"
        data_ext_rets = self.data_ext_rets_root.findall(".//DataExtRet")
        request_counter = 1
        created_count, new_request_counter = add_data_ext_add(self.new_qbxml_msgs, data_ext_rets, parent_id_macro, request_counter)
        self.assertEqual(created_count, 2)
        self.assertEqual(new_request_counter, 3)
        data_ext_add_rqs = self.new_qbxml_msgs.findall(".//DataExtAddRq")
        self.assertEqual(len(data_ext_add_rqs), 2)
        self.assertEqual(data_ext_add_rqs[0].attrib['requestID'], '1')
        txn_data_ext_type = data_ext_add_rqs[0].find(".//TxnDataExtType")
        self.assertEqual(txn_data_ext_type.text, "Invoice")
        txn_id = data_ext_add_rqs[0].find(".//TxnID")
        self.assertEqual(txn_id.attrib['useMacro'], "TxnID:98765")

    def test_add_data_ext_add_with_empty_data_ext_rets(self):
        data_ext_rets = []
        parent_id_macro = "ListID:12345"
        request_counter = 1
        created_count, new_request_counter = add_data_ext_add(self.new_qbxml_msgs, data_ext_rets, parent_id_macro, request_counter)
        self.assertEqual(created_count, 0)
        self.assertEqual(new_request_counter, 1)

    def test_add_data_ext_add_with_incrementing_request_ids(self):
        parent_id_macro = "ListID:12345"
        data_ext_rets = self.data_ext_rets_root.findall(".//DataExtRet")
        request_counter = 5
        created_count, new_request_counter = add_data_ext_add(self.new_qbxml_msgs, data_ext_rets, parent_id_macro, request_counter)
        self.assertEqual(created_count, 2)
        self.assertEqual(new_request_counter, 7)
        data_ext_add_rqs = self.new_qbxml_msgs.findall(".//DataExtAddRq")
        self.assertEqual(data_ext_add_rqs[0].attrib['requestID'], '5')
        self.assertEqual(data_ext_add_rqs[1].attrib['requestID'], '6')


class TestTransformQBXML(unittest.TestCase):

    def setUp(self):
        # Sample XML data to simulate the input structure
        self.xml_data = '''
        <QBXML>
          <QBXMLMsgsRs>
            <CustomerQueryRs requestID="1" statusCode="0" statusSeverity="Info" statusMessage="Status OK">
            <CustomerRet>
              <ListID>12345</ListID>
              <Name>Dunning's Pool Depot, Inc.</Name>
              <IsActive>true</IsActive>
              <CompanyName>Dunning's Pool Depot, Inc.</CompanyName>
              <BillAddress>
                <Addr1>Dunning's Pool Depot, Inc.</Addr1>
                <Addr2>1111 Blast Avenue</Addr2>
                <City>Uptown</City>
                <State>MI</State>
                <PostalCode>55562</PostalCode>
              </BillAddress>
              <ShipAddress>
                <Addr1>Dunning's Pool Depot, Inc.</Addr1>
                <Addr2>1111 Blast Avenue</Addr2>
                <City>Uptown</City>
                <State>MI</State>
                <PostalCode>55562</PostalCode>
              </ShipAddress>
              <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Method</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Overnight</DataExtValue>
              </DataExtRet>
              <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Vendor</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>Fed Ex</DataExtValue>
              </DataExtRet>
              <DataExtRet>
                <OwnerID>0</OwnerID>
                <DataExtName>Ship Account #</DataExtName>
                <DataExtType>STR255TYPE</DataExtType>
                <DataExtValue>877966-6874</DataExtValue>
              </DataExtRet>
            </CustomerRet>
            </CustomerQueryRs>
          </QBXMLMsgsRs>
        </QBXML>
        '''

    def test_transform_qbxml(self):
        # Parse the XML
        root = ET.fromstring(self.xml_data)

        # Call the transform_qbxml function
        new_root = transform_qbxml(root)

        # Find all the AddRq elements
        add_rq_elements = new_root.findall(".//CustomerAddRq")
        data_ext_rq_elements = new_root.findall(".//DataExtAddRq")

        print(ET.tostring(new_root, pretty_print=True).decode())
        # Check that there is exactly 1 CustomerAddRq
        self.assertEqual(len(add_rq_elements), 1)

        # Check that there are exactly 3 DataExtAddRq elements
        self.assertEqual(len(data_ext_rq_elements), 3)

        # Verify that requestIDs are sequential and correct
        expected_request_ids = ['1', '2', '3', '4']
        actual_request_ids = [
            add_rq_elements[0].attrib['requestID'],  # CustomerAddRq
            data_ext_rq_elements[0].attrib['requestID'],  # DataExtAddRq 1
            data_ext_rq_elements[1].attrib['requestID'],  # DataExtAddRq 2
            data_ext_rq_elements[2].attrib['requestID'],  # DataExtAddRq 3
        ]

        self.assertEqual(actual_request_ids, expected_request_ids)

