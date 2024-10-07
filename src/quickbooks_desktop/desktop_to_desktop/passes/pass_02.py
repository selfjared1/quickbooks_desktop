import os
import lxml.etree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.quickbooks_desktop.desktop_to_desktop.utilities import remove_unwanted_tags, convert_ret_to_add, remove_empty_query_responses, add_rq_to_db, process_response_xml


def pass_02_transform_qbxml(session):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_xml")
    response_file_path = os.path.join(folder_path, f'response_pass_02.xml')
    tree = ET.parse(response_file_path)
    root = tree.getroot()
    #todo: IsHomeCurrencyAdjustment may need to be reviewed on if it should say if true
    general_tags_to_remove = ['TimeCreated', 'TimeModified', 'EditSequence', 'TxnNumber', 'IsHomeCurrencyAdjustment',
                              'BillAddressBlock', 'ShipAddressBlock', 'EstimateRet/Subtotal', 'EstimateRet/SalesTaxPercentage',
                              'EstimateRet/SalesTaxTotal', 'EstimateRet/TotalAmount']
    root = remove_empty_query_responses(root)
    root = remove_unwanted_tags(root, general_tags_to_remove)
    # Locate QBXMLMsgsRs and convert it to QBXMLMsgsRq
    qbxml_msgs = root.find("QBXMLMsgsRs")
    qbxml_msgs.tag = "QBXMLMsgsRq"
    qbxml_msgs.set("onError", "stopOnError")


    qbxml_msgs = convert_ret_to_add(qbxml_msgs)
    add_rq_to_db(qbxml_msgs, session)
    # Optionally remove unwanted tags
    last_tags_to_remove = ['ListID']
    qbxml_msgs = remove_unwanted_tags(qbxml_msgs, last_tags_to_remove)

    xml_string = ET.tostring(qbxml_msgs, pretty_print=True, xml_declaration=False, encoding="UTF-8").decode()
    full_xml = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?><QBXML>{xml_string}</QBXML>"""
    # Write the string to a file
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_rq_xml")
    os.makedirs(folder_path, exist_ok=True)
    add_rq_file_path = os.path.join(folder_path, f'add_rq_02.xml')
    with open(add_rq_file_path, 'w') as add_rq_file:
        add_rq_file.write(full_xml)

def pass_02_add_to_qb(qb):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_rq_xml")
    add_rq_file_path = os.path.join(folder_path, f'add_rq_02.xml')
    qb.qbXMLRP = qb.dispatch()
    print('trying begin_session')
    qb.open_connection()
    print('began begin_session')
    qb.begin_session()
    with open(add_rq_file_path, 'r', encoding='utf-8') as file:
        xml_str = file.read()
    try:
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
        response_file_path = os.path.join(folder_path, f'add_rq_02_response.xml')
        with open(response_file_path, 'w') as response_file:
            response_file.write(response)
        # Set up the database session
        engine = create_engine('sqlite:///passes/transaction_mappings.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        process_response_xml(response_file_path, session)
        session.close()
    except Exception as e:
        print(e)
    qb.close_qb()