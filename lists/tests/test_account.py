from lists.Account import Account
import unittest

account_response = """<?xml version="1.0" ?>
<QBXML>
<QBXMLMsgsRs>
<AccountQueryRs requestID="1" statusCode="0" statusSeverity="Info" statusMessage="Status OK">
<AccountRet>
<ListID>20000-896814722</ListID>
<TimeCreated>1998-06-02T13:12:02-07:00</TimeCreated>
<TimeModified>2025-12-15T09:56:40-07:00</TimeModified>
<EditSequence>1765817800</EditSequence>
<Name>Company Checking Account</Name>
<FullName>Company Checking Account</FullName>
<IsActive>true</IsActive>
<Sublevel>0</Sublevel>
<AccountType>Bank</AccountType>
<AccountNumber>1110</AccountNumber>
<Desc>Company Checking Account</Desc>
<Balance>12649.10</Balance>
<TotalBalance>12649.10</TotalBalance>
<TaxLineInfoRet>
<TaxLineID>9920</TaxLineID>
<TaxLineName>&lt;Not tax related&gt;</TaxLineName>
</TaxLineInfoRet>
<CashFlowClassification>NotApplicable</CashFlowClassification>
</AccountRet>
</AccountQueryRs>
</QBXMLMsgsRs>
</QBXML>"""

class TestAccount(unittest.TestCase):
    def test_account(self):
        account = Account.from_xml(account_response)
        self.assertIsInstance(account, Account)
        self.assertEqual(account.ListID, '20000-896814722')
        self.assertEqual(account.TimeCreated, '1998-06-02T13:12:02-07:00')
        self.assertEqual(account.TimeModified, '2025-12-15T09:56:40-07:00')
        self.assertEqual(account.EditSequence, '1765817800')
        self.assertEqual(account.Name, 'Company Checking Account')
        self.assertEqual(account.FullName, 'Company Checking Account')
        self.assertTrue(account.IsActive)
        self.assertEqual(account.Sublevel, 0)
        self.assertEqual(account.AccountType, 'Bank')
        self.assertEqual(account.AccountNumber, '1110')
        self.assertEqual(account.Desc, 'Company Checking Account')
        self.assertEqual(account.Balance, 12649.10)
        self.assertEqual(account.TotalBalance, 12649.10)
        self.assertEqual(account.TaxLineInfoRet.TaxLineID, 9920)
        self.assertEqual(account.TaxLineInfoRet.TaxLineName, '<Not tax related>')
        self.assertEqual(account.CashFlowClassification, 'NotApplicable')
        self.assertIsNone(account.CurrencyRef_ListID)
        self.assertIsNone(account.CurrencyRef_ListFullName)
        self.assertIsNone(account.ParentRef)
        self.assertIsNone(account.BankNumber)
        self.assertIsNone(account.TotalBalance)
        self.assertIsNone(account.TaxLineInfoRet)
        self.assertIsNone(account.CashFlowClassification)
        self.assertIsNone(account.DataExtRet)

