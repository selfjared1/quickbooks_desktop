import unittest
from unittest.mock import patch, MagicMock
from lxml import etree as et
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop, JournalEntry


class TestCopyFromParent(unittest.TestCase):

    def setUp(self):
        self.journal_xml = """
                <JournalEntryRet>
                    <TxnID>19C72-1627671245</TxnID>
                    <TimeCreated>2021-07-30T12:54:05-07:00</TimeCreated>
                    <TimeModified>2022-01-31T15:33:12-07:00</TimeModified>
                    <EditSequence>1627671245</EditSequence>
                    <TxnNumber>34217</TxnNumber>
                    <TxnDate>2005-10-18</TxnDate>
                    <RefNumber>1</RefNumber>
                    <IsAdjustment>false</IsAdjustment>
                    <IsHomeCurrencyAdjustment>false</IsHomeCurrencyAdjustment>
                    <IsAmountsEnteredInHomeCurrency>false</IsAmountsEnteredInHomeCurrency>
                    <CurrencyRef>
                    <ListID>80000096-1622403877</ListID>
                    <FullName>US Dollar</FullName>
                    </CurrencyRef>
                    <ExchangeRate>1</ExchangeRate>
                    <JournalCreditLine>
                    <TxnLineID>19C73-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>80000015-1622404240</ListID>
                    <FullName>Notes - Sample, Inc.</FullName>
                    </AccountRef>
                    <Amount>210000.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalCreditLine>
                    <JournalDebitLine>
                    <TxnLineID>19C74-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>8000005D-1627666939</ListID>
                    <FullName>Automobiles</FullName>
                    </AccountRef>
                    <Amount>4500.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalDebitLine>
                    <JournalDebitLine>
                    <TxnLineID>19C75-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>8000005E-1627666939</ListID>
                    <FullName>Furniture &amp; Fixtures</FullName>
                    </AccountRef>
                    <Amount>2000.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalDebitLine>
                    <JournalDebitLine>
                    <TxnLineID>19C76-1627671245</TxnLineID>
                    <AccountRef>
                    <ListID>8000005C-1627666939</ListID>
                    <FullName>Inventory</FullName>
                    </AccountRef>
                    <Amount>203500.00</Amount>
                    <Memo>original purchase</Memo>
                    </JournalDebitLine>
                </JournalEntryRet>
                """

    def test_copy_from_parent(self):
        element = et.fromstring(self.journal_xml)
        journal_entry = JournalEntry.from_xml(element)
        qb = QuickbooksDesktop()
        jounal_entry_add_w_ids = JournalEntry.Add.create_add_from_parent(journal_entry)
        self.assertTrue(isinstance(jounal_entry_add_w_ids, JournalEntry.Add))
        self.assertEqual(jounal_entry_add_w_ids.ref_number, "1")
        self.assertEqual(jounal_entry_add_w_ids.journal_credit_lines[0].account_ref.full_name, "Notes - Sample, Inc.")

        self.assertFalse(hasattr(jounal_entry_add_w_ids, 'txn_id')) #you can't add with the main txn_id
        self.assertTrue(hasattr(jounal_entry_add_w_ids.currency_ref, 'list_id'))
        self.assertTrue(hasattr(jounal_entry_add_w_ids.journal_credit_lines, 'txn_line_id'))

        jounal_entry_add_wo_ids = JournalEntry.Add.create_add_from_parent(journal_entry, keep_ids=False)
        self.assertFalse(hasattr(jounal_entry_add_wo_ids, 'txn_id'))
        self.assertFalse(hasattr(jounal_entry_add_wo_ids.currency_ref, 'list_id'))
        self.assertFalse(hasattr(jounal_entry_add_wo_ids.journal_credit_lines, 'txn_line_id'))

    #todo: add invoice, so, bill, etc. test to test to make sure lines copy over correctly.

