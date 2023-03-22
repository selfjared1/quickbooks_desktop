import unittest
from datetime import datetime
import pandas as pd
from lists.account import Account
from core.quickbooks_desktop import QuickBooksDesktop

from core.tests.test_session_manager import SessionManager
from lxml import etree as et


class TestAccount(unittest.TestCase):

    def setUp(self):
        super(TestAccount, self).setUp()
        root = et.parse('test_account_data.xml')
        self.response = et.tostring(root, pretty_print=True, encoding='unicode')

        # generates the same accounts as """accounts = qb.get_table('Account')"""


    def test_load(self):
        qb = QuickBooksDesktop()

        # generates the same accounts as """accounts = qb.get_table('Account')"""
        self.accounts = qb.parse_response_xml('Account', self.response)
        self.assertIsInstance(self.accounts, list)
        self.assertIsInstance(self.accounts[0], Account)
        self.assertIsInstance(self.accounts[0].TimeModified, datetime)
        print(self.accounts)
#         root = tree.getroot()
#         # account = Accounts()
#         accounts_df = account.search()
#
#         # account.quick_search(
#         #     account_type='Accounts Payable',
#         # )
#
#         # self.assertTrue(account.account_type == 'Accounts Payable')
#         print('h')
#
# class TestAccountsQuickSearch(TestAccountsCommon):
#
#     def test_accounts_quick_search(self):
#         qb = SessionManager()
#
# class TestAccountsSearch(TestAccountsCommon):
#
#     def test_accounts_search(self):
#         qb = SessionManager()
#
# class TestAccountsUpdate(TestAccountsCommon):
#
#     def test_accounts_update(self):
#         qb = SessionManager()
#
# class TestAccountsAdd(TestAccountsCommon):
#
#     def test_accounts_add(self):
#         qb = SessionManager()

# if __name__ == '__main__':
#     unittest.main()