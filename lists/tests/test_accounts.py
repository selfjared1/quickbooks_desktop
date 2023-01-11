from lists.accounts_marshmallow import Account
from core.quickbooks_desktop import QuickBooksDesktop
import unittest
from core.tests.test_session_manager import SessionManager
from lxml import etree as et

class TestAccount(unittest.TestCase):

    def setUp(self):
        super(TestAccount, self).setUp()
        qb = QuickBooksDesktop()
        root = et.parse('test_account_data.xml')
        xpath = '''/QBXML/QBXMLMsgsRs/AccountQueryRs/AccountRet'''
        self.account_ret = root.xpath(xpath.encode('utf-8'))

    def test_load(self):
        account = Account.from_xml(et.tostring(self.account_ret[0]))
        print(account)
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