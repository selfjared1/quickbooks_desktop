from core.xml_conversion import XmlListToObject
from lxml import etree as et
import unittest

class TestXmlListToObjectCommon(unittest.TestCase):

    def setUp(self):
        super(TestXmlListToObjectCommon, self).setUp()
        self.sample_xml = self.get_sample_xml()

    def get_sample_xml(self):
        print