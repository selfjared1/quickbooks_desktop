import unittest
from core.session_manager import SessionManager

from quickbooks_desktop.session_manager import SessionManager

from lxml import etree as et

class TestSessionManagerCommon(unittest.TestCase):

    def setUp(self):
        super(TestSessionManagerCommon, self).setUp()

class TestSessionManager(TestSessionManagerCommon):

    def test_session_object(self):
        qb = SessionManager()
        self.assertFalse(qb.session_begun)
        self.assertFalse(qb.connection_open)
        self.assertEqual(qb.dispatch_str, "QBXMLRP2.RequestProcessor" )
        self.assertIsNone(qb.qbXMLRP)
        self.assertIsNone(qb.ticket)

        #tear down
        qb = None

    def test_dispatch(self):
        qb = SessionManager()
        qb.dispatch()
        self.assertIsNotNone(qb.qbXMLRP)

        #tear down
        qb = None

    def test_connections(self):
        qb = SessionManager()
        self.assertFalse(qb.connection_open)
        qb.open_connection()
        self.assertTrue(qb.connection_open)

        # tear down
        qb.close_connection()
        self.assertFalse(qb.connection_open)
        qb = None

    def test_session(self):
        qb = SessionManager()
        self.assertFalse(qb.session_begun)
        qb.begin_session()
        self.assertTrue(qb.session_begun)
        self.assertTrue(qb.connection_open)
        self.assertIsNotNone(qb.ticket)

        # Tear Down
        qb.end_session()
        self.assertFalse(qb.session_begun)
        qb.close_connection()
        self.assertFalse(qb.connection_open)
        qb = None

    def test_send_xml(self):
        qb = SessionManager()
        root = et.Element('AccountQueryRq')
        response = qb.send_xml(root)
        print(response)

if __name__ == '__main__':
    unittest.main()