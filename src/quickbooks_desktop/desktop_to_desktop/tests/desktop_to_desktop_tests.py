import unittest
import lxml.etree as ET
from src.quickbooks_desktop.desktop_to_desktop.utilities import remove_unwanted_tags

# Assuming remove_unwanted_tags function is already imported

class TestRemoveUnwantedTags(unittest.TestCase):

    def setUp(self):
        # Sample XML for testing
        self.xml = '''
        <root>
            <FullName>John Doe</FullName>
            <AccountRet>
                <FullName>Account Full Name</FullName>
                <MyFullName>Account My Full Name</MyFullName>
            </AccountRet>
            <CustomerRet>
                <FullName>Account Full Name</FullName>
                <MyFullName>Customer My Full Name</MyFullName>
            </CustomerRet>
        </root>
        '''
        self.root = ET.fromstring(self.xml)

    def test_remove_exact_fullname(self):
        # Test exact removal of 'FullName'
        tags_to_remove = ['FullName']
        modified_root = remove_unwanted_tags(self.root, tags_to_remove)
        self.assertIsNone(modified_root.find('.//FullName'))  # Ensure FullName is removed
        self.assertIsNotNone(modified_root.find('.//MyFullName'))  # Ensure MyFullName remains

    def test_remove_exact_accountret_fullname(self):
        # Test exact removal of 'AccountRet/FullName'
        tags_to_remove = ['AccountRet/FullName']
        modified_root = remove_unwanted_tags(self.root, tags_to_remove)
        self.assertIsNone(modified_root.find('.//AccountRet/FullName'))  # Ensure AccountRet/FullName is removed
        self.assertIsNotNone(modified_root.find('.//CustomerRet/FullName'))  # Ensure CustomerRet/FullName remains
        self.assertIsNotNone(modified_root.find('.//AccountRet/MyFullName'))  # Ensure MyFullName remains

    def test_remove_wildcard_accountret_myfullname(self):
        # Test removal of 'AccountRet/*FullName' (should remove AccountRet/MyFullName)
        tags_to_remove = ['AccountRet/*FullName']
        modified_root = remove_unwanted_tags(self.root, tags_to_remove)
        self.assertIsNone(modified_root.find('.//AccountRet/MyFullName'))  # Ensure AccountRet/MyFullName is removed
        self.assertIsNotNone(modified_root.find('.//CustomerRet/MyFullName'))  # Ensure CustomerRet/MyFullName remains

    def test_remove_global_wildcard_myfullname(self):
        # Test removal of '*MyFullName' (should remove all elements ending with MyFullName)
        tags_to_remove = ['*MyFullName']
        modified_root = remove_unwanted_tags(self.root, tags_to_remove)
        self.assertIsNone(modified_root.find('.//AccountRet/MyFullName'))  # Ensure AccountRet/MyFullName is removed
        self.assertIsNone(modified_root.find('.//CustomerRet/MyFullName'))  # Ensure CustomerRet/MyFullName is removed
