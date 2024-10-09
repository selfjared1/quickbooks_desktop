import os
import lxml.etree as ET
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.quickbooks_desktop.desktop_to_desktop.utilities import remove_unwanted_tags, convert_ret_to_add_or_mod
from src.quickbooks_desktop.desktop_to_desktop.utilities import remove_empty_query_responses, process_response_xml
from src.quickbooks_desktop.desktop_to_desktop.utilities import remove_amount_from_subtotals, truncate_tag_text, remove_uncle_tag_based_on_xpath
from src.quickbooks_desktop.desktop_to_desktop.utilities import reorder_specific_tag_in_document, only_keep_child_tags
from src.quickbooks_desktop.desktop_to_desktop.add_rq_to_db import add_rq_to_db
from src.quickbooks_desktop.desktop_to_desktop.clean_xml import clean_text
from src.quickbooks_desktop.desktop_to_desktop.models import TransactionMapping

def pass_02_transform_qbxml(session):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_xml")
    response_file_path = os.path.join(folder_path, f'response_pass_02.xml')
    tree = ET.parse(response_file_path)
    root = tree.getroot()
    #todo: IsHomeCurrencyAdjustment may need to be reviewed on if it should say if true
    general_tags_to_remove = ['TimeCreated', 'TimeModified', 'EditSequence', 'TxnNumber', 'EstimateRet/IsHomeCurrencyAdjustment',
                              'EstimateRet/BillAddressBlock', 'ShipAddressBlock', 'EstimateRet/Subtotal', 'EstimateRet/SalesTaxPercentage',
                              'EstimateRet/SalesTaxTotal', 'EstimateRet/TotalAmount', 'VendorAddressBlock',
                              'PurchaseOrderRet/TotalAmount', 'EstimateRet/IsManuallyClosed', 'EstimateRet/IsFullyReceived', 'PurchaseOrderRet/LinkedTxn',
                              'PurchaseOrderLineRet/ReceivedQuantity', 'PurchaseOrderLineRet/IsBilled',
                              'PurchaseOrderLineRet/OverrideUOMSetRef', 'EstimateRet/CurrencyRef', 'EstimateRet/TotalAmountInHomeCurrency',
                               'EstimateLineGroupRet/IsPrintItemsInGroup', 'EstimateLineGroupRet/TotalAmount',
                              'EstimateLineGroupRet/Desc', 'EstimateLineGroupRet/EstimateLineRet', 'PurchaseOrderRet/TotalAmount',
                              'PurchaseOrderRet/CurrencyRef', 'PurchaseOrderRet/TotalAmountInHomeCurrency', 'PurchaseOrderRet/IsManuallyClosed',
                              'PurchaseOrderRet/PurchaseOrderLineRet/IsManuallyClosed', 'PurchaseOrderRet/IsFullyReceived',
                              'PurchaseOrderRet/ShipToEntityRef', 'PurchaseOrderLineGroupRet/Desc', 'PurchaseOrderLineGroupRet/IsPrintItemsInGroup',
                              'PurchaseOrderLineGroupRet/TotalAmount', 'PurchaseOrderLineRet/IsManuallyClosed',
                              'PurchaseOrderLineGroupRet/PurchaseOrderLineRet']


    root = remove_empty_query_responses(root)
    root = remove_unwanted_tags(root, general_tags_to_remove)
    delete_uncles_list = {
        'Total Avatax': 'Rate'
    }

    for item_name, uncle_to_remove in delete_uncles_list.items():
        search_xpath = f".//*[substring(local-name(), string-length(local-name()) - string-length('LineAdd') + 1) = 'LineAdd']/ItemRef/FullName[text()='{item_name}']"
        root = remove_uncle_tag_based_on_xpath(root, search_xpath, uncle_to_remove)
    # Locate QBXMLMsgsRs and convert it to QBXMLMsgsRq
    list_of_subtotal_items = ['Reimb Subt', 'Amount Subtotal']
    remove_amount_from_subtotals(root, list_of_subtotal_items)
    # line_elements = root.xpath(".//*[substring(name(), string-length(name()) - 6) = 'LineRet']")
    # for line_element in line_elements:
    #     print(ET.tostring(line_element))

    qbxml_msgs = root.find("QBXMLMsgsRs")
    qbxml_msgs.tag = "QBXMLMsgsRq"
    qbxml_msgs.set("onError", "stopOnError")


    qbxml_msgs = convert_ret_to_add_or_mod(qbxml_msgs, session, 'Add')
    print('finished convert_ret_to_add')
    add_rq_to_db(qbxml_msgs, session)
    # Optionally remove unwanted tags
    last_tags_to_remove = ['ListID', 'DataExtRet']
    qbxml_msgs = remove_unwanted_tags(qbxml_msgs, last_tags_to_remove)

    so_tag_order_list = ['ItemSalesTaxRef', 'Memo', 'CustomerMsgRef', 'IsToBeEmailed', 'CustomerSalesTaxCodeRef', 'Other',
                      'ExchangeRate', 'ExternalGUID']
    reorder_specific_tag_in_document(qbxml_msgs, 'EstimateAdd', so_tag_order_list, 'ExchangeRate')

    po_tag_order_list = ['DueDate', 'ExpectedDate', 'ShipMethodRef', 'FOB', 'Memo', 'VendorMsg', 'IsToBePrinted',
                         'IsToBeEmailed', 'Other1', 'Other2', 'ExchangeRate', 'ExternalGUID']
    reorder_specific_tag_in_document(qbxml_msgs, 'PurchaseOrderAdd', po_tag_order_list, 'ExchangeRate')

    tags_to_truncate = {'Addr1': 39,
                        'Addr2': 39,
                        }
    for tag, length in tags_to_truncate.items():
        qbxml_msgs = truncate_tag_text(qbxml_msgs, tag, length)


    xml_string = ET.tostring(qbxml_msgs, pretty_print=True, xml_declaration=False, encoding="UTF-8").decode()
    xml_string = clean_text(xml_string)
    full_xml = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?><QBXML>{xml_string}</QBXML>"""
    # Write the string to a file
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_rq_xml")
    os.makedirs(folder_path, exist_ok=True)
    add_rq_file_path = os.path.join(folder_path, f'add_rq_02.xml')
    with open(add_rq_file_path, 'w', encoding='utf-8') as add_rq_file:
        add_rq_file.write(full_xml)
    print('finished tranform_qbxml')

def pass_02_add_to_qb(qb):
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_rq_xml")
    add_rq_file_path = os.path.join(folder_path, f'add_rq_02.xml')
    with open(add_rq_file_path, 'r', encoding='utf-8') as file:
        xml_str = file.read()
        # print(xml_str)
    try:
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
        print(response[:100])
        response_file_path = os.path.join(folder_path, f'add_rq_02_response.xml')
        with open(response_file_path, 'w') as response_file:
            response_file.write(response)

    except Exception as e:
        print(e)

def pass_02_process_response_xml():
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_rq_xml")
    response_file_path = os.path.join(folder_path, f'add_rq_02_response.xml')
    with open(response_file_path, 'r', encoding='utf-8') as file:
        xml_str = file.read()

    engine = create_engine('sqlite:///passes/transaction_mappings.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    process_response_xml(response_file_path, session)
    session.close()

def pass_02_mod_line_groups():
    engine = create_engine('sqlite:///passes/transaction_mappings.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_xml")
    response_file_path = os.path.join(folder_path, f'response_pass_02.xml')
    tree = ET.parse(response_file_path)
    root = tree.getroot()
    # look for parents of children with tags that end in LIneGroupRet
    tags_to_keep = ['TxnID', 'PurchaseOrderLineGroupRet', 'EstimateLineGroupRet']

    transactions_to_mod_rets = root.findall(".//*[ *[ends-with(local-name(), 'LineGroupRet')] ]")
    for transaction_element in transactions_to_mod_rets:
        transaction_type_name = str(transaction_element.tag).replace('Ret', '')
        old_qb_trx_id = transaction_element.find('TrxID').tag
        mappings = session.query(TransactionMapping).filter_by(
            old_qb_trx_id=old_qb_trx_id
        ).all()
        only_keep_child_tags(transaction_element, tags_to_keep)
        list_of_line_id_elements = root.findall(".//*[ends-with(local-name(), 'lineID')]")
        for line_id_element in list_of_line_id_elements:
            for mapping in mappings:
                if mapping.old_qb_trx_line_id == line_id_element.tag:
                    line_id_element.tag = mapping.new_qb_trx_line_id
                else:
                    pass

    tags_to_remove = ['ListID', 'EstimateLineGroupRet/Desc', 'EstimateLineGroupRet/IsPrintItemsInGroup', 'EstimateLineGroupRet/TotalAmount',
                      'EstimateLineRet/DataExtRet']
    root = remove_unwanted_tags(root, tags_to_remove)
    qbxml_msgs = root.find("QBXMLMsgsRs")
    qbxml_msgs.tag = "QBXMLMsgsRq"
    qbxml_msgs.set("onError", "stopOnError")
    convert_ret_to_add_or_mod(qbxml_msgs, session, 'Add')






    session.close()





    root = remove_empty_query_responses(root)
    root = remove_unwanted_tags(root, general_tags_to_remove)
    delete_uncles_list = {
        'Total Avatax': 'Rate'
    }

    for item_name, uncle_to_remove in delete_uncles_list.items():
        search_xpath = f".//*[substring(local-name(), string-length(local-name()) - string-length('LineAdd') + 1) = 'LineAdd']/ItemRef/FullName[text()='{item_name}']"
        root = remove_uncle_tag_based_on_xpath(root, search_xpath, uncle_to_remove)
    # Locate QBXMLMsgsRs and convert it to QBXMLMsgsRq
    list_of_subtotal_items = ['Reimb Subt', 'Amount Subtotal']
    remove_amount_from_subtotals(root, list_of_subtotal_items)
    # line_elements = root.xpath(".//*[substring(name(), string-length(name()) - 6) = 'LineRet']")
    # for line_element in line_elements:
    #     print(ET.tostring(line_element))

    qbxml_msgs = root.find("QBXMLMsgsRs")
    qbxml_msgs.tag = "QBXMLMsgsRq"
    qbxml_msgs.set("onError", "stopOnError")

    qbxml_msgs = convert_ret_to_add_or_mod(qbxml_msgs, session, 'Add')
    print('finished convert_ret_to_add')
    add_rq_to_db(qbxml_msgs, session)
    # Optionally remove unwanted tags
    last_tags_to_remove = ['ListID', 'DataExtRet']
    qbxml_msgs = remove_unwanted_tags(qbxml_msgs, last_tags_to_remove)

    so_tag_order_list = ['ItemSalesTaxRef', 'Memo', 'CustomerMsgRef', 'IsToBeEmailed', 'CustomerSalesTaxCodeRef',
                         'Other',
                         'ExchangeRate', 'ExternalGUID']
    reorder_specific_tag_in_document(qbxml_msgs, 'EstimateAdd', so_tag_order_list, 'ExchangeRate')

    po_tag_order_list = ['DueDate', 'ExpectedDate', 'ShipMethodRef', 'FOB', 'Memo', 'VendorMsg', 'IsToBePrinted',
                         'IsToBeEmailed', 'Other1', 'Other2', 'ExchangeRate', 'ExternalGUID']
    reorder_specific_tag_in_document(qbxml_msgs, 'PurchaseOrderAdd', po_tag_order_list, 'ExchangeRate')

    tags_to_truncate = {'Addr1': 39,
                        'Addr2': 39,
                        }
    for tag, length in tags_to_truncate.items():
        qbxml_msgs = truncate_tag_text(qbxml_msgs, tag, length)

    xml_string = ET.tostring(qbxml_msgs, pretty_print=True, xml_declaration=False, encoding="UTF-8").decode()
    xml_string = clean_text(xml_string)
    full_xml = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?><QBXML>{xml_string}</QBXML>"""
    # Write the string to a file
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_rq_xml")
    os.makedirs(folder_path, exist_ok=True)
    add_rq_file_path = os.path.join(folder_path, f'add_rq_02.xml')
    with open(add_rq_file_path, 'w', encoding='utf-8') as add_rq_file:
        add_rq_file.write(full_xml)
    print('finished tranform_qbxml')
