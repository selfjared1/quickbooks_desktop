import unittest
from unittest.mock import patch, MagicMock
from lxml import etree as et
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
from src.quickbooks_desktop.transactions import JournalEntry


class TestQuickbooksDesktop(unittest.TestCase):
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
            <FullName>Notes - Artco, Inc.</FullName>
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

    def test_add_journal_entry(self):
        qb = QuickbooksDesktop()
        qb.qbXMLRP = qb.dispatch()
        print('trying begin_session')
        qb.open_connection()
        print('began begin_session')
        qb.begin_session()
        journal_entry = JournalEntry.from_xml(self.journal_xml)
        journal_entry.save(qb)
        qb.close_connection()