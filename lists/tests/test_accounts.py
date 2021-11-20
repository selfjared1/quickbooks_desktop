from lists.accounts import Accounts
import unittest
from core.test_session_manager import SessionManager

class TestAccountsCommon(unittest.TestCase):

    def setUp(self):
        super(TestAccountsCommon, self).setUp()
        account = Accounts()
        account.search(
            account_type='Accounts Payable',
        )
        self.assertTrue(account.account_type == 'Accounts Payable')
        print('h')

class TestAccountsSearch(TestAccountsCommon):

    def test_account_search(self):
        qb = SessionManager()

class TestAccountsUpdate(TestAccountsCommon):

    def test_session_object(self):
        qb = SessionManager()

class TestAccountsAdd(TestAccountsCommon):

    def test_session_object(self):
        qb = SessionManager()