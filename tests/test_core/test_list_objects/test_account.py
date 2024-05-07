import unittest
from lxml import etree as et

from core.list_objects.qb_account import QBAccount

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = QBAccount()
        super(TestAccount, self).setUp()
        root = et.parse('test_account_data.xml')
        self.response = et.tostring(root, pretty_print=True, encoding='unicode')

    def test_valid_lengths(self):
        """ Test that valid lengths do not raise any exceptions """
        try:
            self.account.EditSequence = '1234567890123456'  # Max 16 chars
            self.account.Name = 'John Doe'  # Max 31 chars
            self.account.FullName = 'John Doe ' * 10  # Max 159 chars
            self.account.AccountNumber = '1234567'  # Max 7 chars
            self.account.BankNumber = '123456789012345'  # Max 25 chars
            self.account.Desc = 'This is a valid description'  # Max 200 chars
        except ValueError:
            self.fail("Valid lengths are raising exceptions")


    # def test_load(self):
    #     qb = QuickBooksDesktop()
    #
    #     # generates the same accounts as """accounts = qb.get_table('Account')"""
    #     self.accounts = qb.parse_response_xml('Account', self.response)
    #     self.assertIsInstance(self.accounts, list)
    #     self.assertIsInstance(self.accounts[0], Account)
    #     self.assertIsInstance(self.accounts[0].TimeModified, datetime)
    #     print(self.accounts)
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