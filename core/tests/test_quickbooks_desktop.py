from core.mixins import XmlListToObject
from lxml import etree as et
from core.quickbooks_desktop import QuickBooksDesktop
import unittest

class TestQuickbooksDesktop(unittest.TestCase):

    def setUp(self) -> None:
        self.qb = QuickBooksDesktop()

    def test_get_table(self):
        # Test only works if a quickbooks company file is open
        pass

class TestXmlListToObjectCommon(unittest.TestCase):

    def setUp(self):
        super(TestXmlListToObjectCommon, self).setUp()
        self.sample_xml = self.get_sample_xml()

    def get_sample_xml(self):
        print