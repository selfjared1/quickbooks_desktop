import unittest
from unittest.mock import patch, MagicMock
from lxml import etree as et
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop  # Assuming your class is in a module called quickbooks_desktop


class TestQuickbooksDesktop(unittest.TestCase):

    @patch('src.quickbooks_desktop.quickbooks_desktop.win32com.client.Dispatch')
    def test_dispatch_without_company_file(self, mock_dispatch):
        qb_desktop = QuickbooksDesktop()
        qb_desktop.dispatch()

        # Check that Dispatch was called
        mock_dispatch.assert_called_once_with("QBXMLRP2.RequestProcessor")
        self.assertIsNotNone(qb_desktop.qbXMLRP)

    @patch('src.quickbooks_desktop.quickbooks_desktop.win32com.client.Dispatch')
    def test_dispatch_with_company_file(self, mock_dispatch):
        qb_desktop = QuickbooksDesktop(company_file="path/to/company.qbw")
        qb_desktop.dispatch()

        # Since the company file functionality is not implemented, test that the output is "company file isn't an option right now"
        with patch('builtins.print') as mocked_print:
            qb_desktop.dispatch()
            mocked_print.assert_called_once_with("company file isn't an option right now")

    @patch('src.quickbooks_desktop.quickbooks_desktop.win32com.client.Dispatch')
    def test_open_connection(self, mock_dispatch):
        qb_desktop = QuickbooksDesktop()
        mock_qbXMLRP = MagicMock()
        qb_desktop.qbXMLRP = mock_qbXMLRP

        qb_desktop.open_connection()

        # Ensure that OpenConnection2 is called with proper parameters
        mock_qbXMLRP.OpenConnection2.assert_called_once_with('', 'accountingpy', 1)
        self.assertTrue(qb_desktop.connection_open)

    @patch('src.quickbooks_desktop.quickbooks_desktop.win32com.client.Dispatch')
    def test_begin_session(self, mock_dispatch):
        qb_desktop = QuickbooksDesktop()
        mock_qbXMLRP = MagicMock()
        qb_desktop.qbXMLRP = mock_qbXMLRP
        qb_desktop.connection_open = True

        # Begin the session
        qb_desktop.begin_session()
        mock_qbXMLRP.BeginSession.assert_called_once_with("", 0)
        self.assertTrue(qb_desktop.session_begun)

    def test_convert_to_lxml_from_string(self):
        qb_desktop = QuickbooksDesktop()
        xml_string = "<Request><Data>Test</Data></Request>"

        result = qb_desktop._convert_to_lxml(xml_string)

        # Check if result is properly converted to lxml.etree.Element
        self.assertIsInstance(result, et._Element)
        self.assertEqual(result.tag, "Request")

    def test_convert_to_lxml_from_etree(self):
        qb_desktop = QuickbooksDesktop()
        root = et.Element("Request")
        child = et.SubElement(root, "Data")
        child.text = "Test"
        requestXML = et.ElementTree(root)

        result = qb_desktop._convert_to_lxml(requestXML)

        # Check if result is properly converted to lxml.etree.Element
        self.assertIsInstance(result, et._Element)
        self.assertEqual(result.tag, "Request")

    def test_ensure_qbxml_structure(self):
        qb_desktop = QuickbooksDesktop()
        root = et.Element("TestRequest")

        QBXML, QBXMLMsgsRq = qb_desktop._ensure_qbxml_structure(root)

        # Ensure QBXML structure is correct
        self.assertEqual(QBXML.tag, "QBXML")
        self.assertEqual(QBXMLMsgsRq.tag, "QBXMLMsgsRq")
        self.assertEqual(QBXMLMsgsRq.get("onError"), "stopOnError")

    @patch('src.quickbooks_desktop.quickbooks_desktop.win32com.client.Dispatch')
    def test_send_xml(self, mock_dispatch):
        qb_desktop = QuickbooksDesktop()
        mock_qbXMLRP = MagicMock()
        qb_desktop.qbXMLRP = mock_qbXMLRP

        # Mock the QBXMLRP ProcessRequest
        mock_qbXMLRP.ProcessRequest.return_value = "<QBXML><QBXMLMsgsRs/></QBXML>"

        # Test with a simple requestXML
        requestXML = "<TestRequest><Data>Test</Data></TestRequest>"

        result = qb_desktop.send_xml(requestXML)

        # Ensure that the connection was opened and request was processed
        mock_qbXMLRP.ProcessRequest.assert_called_once()
        self.assertIsNotNone(result)

    @patch('src.quickbooks_desktop.quickbooks_desktop.win32com.client.Dispatch')
    def test_close_qb(self, mock_dispatch):
        qb_desktop = QuickbooksDesktop()
        mock_qbXMLRP = MagicMock()
        qb_desktop.qbXMLRP = mock_qbXMLRP
        qb_desktop.session_begun = True
        qb_desktop.connection_open = True

        # Call close_qb
        qb_desktop.close_qb()

        # Ensure that both end_session and close_connection were called
        mock_qbXMLRP.EndSession.assert_called_once()
        mock_qbXMLRP.CloseConnection.assert_called_once()
        self.assertFalse(qb_desktop.session_begun)
        self.assertFalse(qb_desktop.connection_open)


if __name__ == '__main__':
    unittest.main()
