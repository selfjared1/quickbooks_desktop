import os
from lxml import etree
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop


# Function to query the table and get TxnIDs
def get_txn_ids(qb, table_name):
    # Construct the query XML to fetch TxnID only
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="stopOnError">
            <{table_name}QueryRq requestID="1">
                <IncludeRetElement>TxnID</IncludeRetElement>
            </{table_name}QueryRq>
        </QBXMLMsgsRq>
    </QBXML>"""

    try:
        # Send the query request to QuickBooks and get the response
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
        print(f"Response for {table_name} query: {response}")

        # Parse the response to extract all TxnID elements
        parser = etree.XMLParser(remove_blank_text=True)
        root = etree.fromstring(response, parser)

        # Extract all TxnID elements
        txn_ids = root.xpath(f"//TxnID")
        txn_id_list = [txn.text for txn in txn_ids]  # Get the text value of each TxnID

        print(f"Found {len(txn_id_list)} TxnID(s) for {table_name}")
        return txn_id_list

    except Exception as e:
        print(f"Error querying {table_name}: {e}")
        return []


# Function to delete transactions using TxnDelRq
def delete_transactions(qb, table_name, txn_ids):
    # Loop through each TxnID and send a delete request
    TxnDelRqs = ''
    for i, txn_id in enumerate(txn_ids, start=1):
        # Create the TxnDelRq XML string with a unique requestID
        xml_str = f"""
            <TxnDelRq requestID="{i}">
                <TxnDelType>{table_name}</TxnDelType>
                <TxnID>{txn_id}</TxnID>
            </TxnDelRq>
        """
        TxnDelRqs += xml_str

    xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                {TxnDelRqs}
            </QBXMLMsgsRq>
        </QBXML>"""
    try:
        # Send the TxnDelRq request to QuickBooks
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
        print(f"Response from QuickBooks for {table_name} deletion: {response}")

    except Exception as e:
        print(f"Error deleting {table_name} transaction: {e}")


# Higher-level function to combine both querying and deleting transactions
def query_and_delete_transactions(qb, data_transfer_dict):
    for table_name in data_transfer_dict.keys():
        print(f"Processing {table_name}...")

        # Step 1: Get the list of TxnID from the table
        txn_ids = get_txn_ids(qb, table_name)

        # Step 2: Delete each transaction based on the retrieved TxnID
        if txn_ids:
            delete_transactions(qb, table_name, txn_ids)
        else:
            print(f"No TxnIDs found for {table_name}, skipping deletion.")

if __name__ == '__main__':

    # Example usage:
    qb = QuickbooksDesktop()
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    qb.begin_session()
    data_transfer_dict = {
        "Bill": {},  # Example to process Invoice table
    }

    # Run the query and deletion process
    try:
        query_and_delete_transactions(qb, data_transfer_dict)
    except Exception as e:
        print(e)
    qb.close_qb()
