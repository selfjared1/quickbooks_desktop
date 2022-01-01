from lists.accounts_old import Accounts
import unittest
from core.tests.test_session_manager import SessionManager

class TestAccountsCommon(unittest.TestCase):

    def setUp(self):
        super(TestAccountsCommon, self).setUp()
        account = Accounts()
        accounts_df = account.quick_search()

        # account.quick_search(
        #     account_type='Accounts Payable',
        # )

        # self.assertTrue(account.account_type == 'Accounts Payable')
        print('h')

class TestAccountsQuickSearch(TestAccountsCommon):

    def test_account_quick_search(self):
        qb = SessionManager()

class TestAccountsSearch(TestAccountsCommon):

    def test_account_search(self):
        qb = SessionManager()

class TestAccountsUpdate(TestAccountsCommon):

    def test_account_update(self):
        qb = SessionManager()

class TestAccountsAdd(TestAccountsCommon):

    def test_account_add(self):
        qb = SessionManager()