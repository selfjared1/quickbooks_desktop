import os
from src.quickbooks_desktop.desktop_to_desktop.resources_dict import get_list_of_lists, get_list_of_transactions
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop

def build_queries():
    list_of_lists = get_list_of_lists()
    queries = ''
    request_id = 1
    for list_table in list_of_lists:
        query = f"""<{list_table}QueryRq requestID="{request_id}">
                <ActiveStatus>All</ActiveStatus>
                <OwnerID>0</OwnerID>
            </{list_table}QueryRq>"""
        queries += query
        request_id += 1

    transactions_list = get_list_of_transactions()
    for transaction_table in transactions_list:
        query = f"""<{transaction_table}QueryRq requestID="{request_id}">
                        <IncludeLineItems>true</IncludeLineItems>
                        <IncludeLinkedTxns>true</IncludeLinkedTxns>
                        <OwnerID>0</OwnerID>
                    </{transaction_table}QueryRq>"""
        queries += query
        request_id += 1
    return queries




def query_all(response_file_path):

    queries = build_queries()
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
                    <QBXML>
                        <QBXMLMsgsRq onError="stopOnError">
                            {queries}
                        </QBXMLMsgsRq>
                    </QBXML>"""
    qb = QuickbooksDesktop()
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    qb.begin_session()
    try:
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)

        with open(response_file_path, 'w') as response_file:
            response_file.write(response)
    except Exception as e:
        print(e)
    qb.close_qb()



