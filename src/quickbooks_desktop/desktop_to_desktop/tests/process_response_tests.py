import unittest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.quickbooks_desktop.desktop_to_desktop.utilities import process_response_xml
from src.quickbooks_desktop.desktop_to_desktop.models import TransactionMapping, Base


class TestProcessResponseXml(unittest.TestCase):
    def setUp(self):
        # Set up an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Insert a sample TransactionMapping entry
        mapping = TransactionMapping(
            request_id=1,  # Matching the requestID in the sample XML
            qb_add_rq_name='JournalEntryAdd',
            old_qb_trx_id='19C72-1627671245'
        )
        self.session.add(mapping)

        line_mapping_01 = TransactionMapping(
            request_id=1,  # Matching the requestID in the sample XML
            qb_add_rq_name='JournalEntryAdd',
            old_qb_trx_id='19C72-1627671246'
        )
        self.session.add(line_mapping_01)
        line_mapping_02 = TransactionMapping(
            request_id=1,  # Matching the requestID in the sample XML
            qb_add_rq_name='JournalEntryAdd',
            old_qb_trx_id='19C72-1627671247'
        )
        self.session.add(line_mapping_02)
        self.session.commit()

        # Prepare a sample XML response
        self.response_xml = """<?xml version="1.0" ?>
    <QBXML>
        <QBXMLMsgsRs>
            <JournalEntryAddRs requestID="1" statusCode="0" statusSeverity="Info" statusMessage="Status OK">
            <JournalEntryRet>
                <TxnID>BF5E-1828899527</TxnID>
                <TimeCreated>2027-12-15T12:38:47-07:00</TimeCreated>
                <TimeModified>2027-12-15T12:38:47-07:00</TimeModified>
                <EditSequence>1828899527</EditSequence>
                <TxnNumber>1377</TxnNumber>
                <TxnDate>2026-12-29</TxnDate>
                <RefNumber>Interest</RefNumber>
                <IsAdjustment>false</IsAdjustment>
                <JournalCreditLine>
                    <TxnLineID>BF5F-1828899527</TxnLineID>
                    <AccountRef>
                        <ListID>670002-1041541147</ListID>
                        <FullName>Line of Credit</FullName>
                    </AccountRef>
                    <Amount>60.27</Amount>
                </JournalCreditLine>
                <JournalDebitLine>
                    <TxnLineID>BF60-1828899527</TxnLineID>
                    <AccountRef>
                        <ListID>550000-994887129</ListID>
                        <FullName>Other Expense:Interest Expense</FullName>
                    </AccountRef>
                    <Amount>60.27</Amount>
                </JournalDebitLine>
            </JournalEntryRet>
        </JournalEntryAddRs>
        </QBXMLMsgsRs>
    </QBXML>"""
        # Write the sample XML to a temporary file
        self.response_file_path = 'test_response.xml'
        with open(self.response_file_path, 'w', encoding='utf-8') as f:
            f.write(self.response_xml)

    def tearDown(self):
        # Close the session and remove the temporary file
        self.session.close()
        os.remove(self.response_file_path)

    def test_process_01_response(self):
        # Modify the process_response_xml function to accept a session parameter
        # For testing purposes, we can create a wrapper function

            # Close the session (handled in tearDown)

        # Call the modified function with the testing session
        process_response_xml(self.response_file_path, self.session)

        # Verify that the database has been updated correctly
        mapping = self.session.query(TransactionMapping).filter_by(
            request_id=1,
            qb_add_rq_name='JournalEntryAdd'
        ).first()
        self.assertIsNotNone(mapping)
        self.assertEqual(mapping.new_qb_trx_id, 'BF5E-1828899527')

        mappings = self.session.query(TransactionMapping).filter_by(
            request_id=1,
            qb_add_rq_name='JournalEntryAdd'
        ).all()
        self.assertEqual(mappings[0].new_qb_trx_id, 'BF5E-1828899527')
        self.assertEqual(mappings[0].new_qb_trx_line_id, 'BF5F-1828899527')
        self.assertEqual(mappings[1].new_qb_trx_id, 'BF5E-1828899527')
        self.assertEqual(mappings[1].new_qb_trx_line_id, 'BF60-1828899527')



