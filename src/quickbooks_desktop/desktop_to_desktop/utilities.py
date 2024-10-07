
import os
import lxml.etree as ET
from src.quickbooks_desktop.desktop_to_desktop.models import TransactionMapping
from src.quickbooks_desktop.desktop_to_desktop.query_all import query_all
from burn.phone_notifications import notify_jared_process_is_done
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

#Info on things that need to be done manually:
    #Add currency exchange rates
def transfer_lists():
    pass_list = [
        'Account',
        'BillingRate',
        'Class',
        'Currency',
        'Customer',
        'CustomerMsg',
        'CustomerType',
        'DateDrivenTerms',
        'Employee',
        'InventorySite',
        'ItemDiscount',
        'ItemFixedAsset',
        'ItemGroup',
        'ItemInventory',
        'ItemInventoryAssembly',
        'ItemNonInventory',
        'ItemOtherCharge',
        'ItemPayment',
        'ItemSalesTax',
        'ItemSalesTaxGroup',
        'ItemService',
        'ItemSubtotal',
        'JobType',
        'OtherName',
        'PaymentMethod',
        'PayrollItemWage',
        'PriceLevel',
        'SalesRep',
        'SalesTaxCode',
        'ShipMethod',
        'StandardTerms',
        'UnitOfMeasureSet',
        'Vehicle',
        'Vendor',
        'VendorType',
        'WorkersCompCode'
    ]

def pass_01():
    pass_list = [
        "TimeTracking",
        "VehicleMileage",
        "JournalEntry",  # because journals can have ap and ar related transactions
    ]

def pass_02():
    pass_list = [
        "TimeTracking",
        "VehicleMileage",
        "Estimate",
        "PurchaseOrder",
    ]

def pass_03():
    pass_list = [
        "SalesOrder",
        "ItemReceipt",
    ]

def pass_04():
    # because you purchase stuff before you can sell it
    pass_list = [
        "Bill",
        "VendorCredit",
    ]

def pass_05():
    # because you build stuff after you purchase it
    pass_list = [
        "BuildAssembly",
    ]

def pass_06():
    # because you adjust then transfer inventory before you sell it
    pass_list = [
        "InventoryAdjustment",
        "TransferInventory",
        "Transfer",  # missing in the original list
    ]

def pass_07():
    # sell stuff
    pass_list = [
        "Invoice",
        "SalesReceipt",
    ]

def pass_08():
    # get paid
    pass_list = [
        "CreditMemo",
        "ARRefundCreditCard",
        "ReceivePayment",
        "Deposit",
    ]

def pass_09():
    # spend money after you get paid
    pass_list = [
        "Charge",  # because sometimes they have ap accounts and need to be referenced
        "Check",  # because sometimes they have ap accounts and need to be referenced
        "CreditCardCharge",  # because sometimes they have ap accounts and need to be referenced
        "CreditCardCredit",
    ]

def pass_10():
    # pay bills
    pass_list = [
        "BillPaymentCheck",
        "BillPaymentCreditCard",
        "SalesTaxPaymentCheck",
    ]

def add_journal_line_to_db(add, request_id, qb_table_name, session):
    txn_line_id_elements = add.xpath('.//TxnLineID')
    for txn_line_id_elem in txn_line_id_elements:
        parent = txn_line_id_elem.getparent()
        if parent.tag in ['JournalCreditLine', 'JournalDebitLine']:
            old_qb_id = txn_line_id_elem.text
            mapping = TransactionMapping(
                request_id=request_id,
                qb_add_rq_name=qb_table_name,
                is_trx_line_id=True,
                old_qb_id=old_qb_id
            )
            session.add(mapping)
            parent.remove(txn_line_id_elem)
        else:
            pass

def add_line_ret_to_db(add, request_id, qb_table_name, session):
    # txn_line_id_elements = add.xpath('.//TxnLineID')
    txn_line_ret_elements = add.xpath(
        ".//*[substring(local-name(), string-length(local-name()) - string-length('LineRet') + 1) = 'LineRet']"
    )

    for txn_line_ret in txn_line_ret_elements:
        if txn_line_ret[0].tag[-6:] == 'LineID':
            txn_line_id_elem = txn_line_ret[0]
            old_qb_id = txn_line_id_elem.text
            mapping = TransactionMapping(
                request_id=request_id,
                qb_add_rq_name=qb_table_name,
                is_trx_line_id=True,
                old_qb_id=old_qb_id
            )
            session.add(mapping)
            txn_line_id_elem.getparent().remove(txn_line_id_elem)
        else:
            pass
        txn_line_ret.tag = txn_line_ret.tag.replace('Ret', 'Add')

def add_rq_to_db(qbxml_msgs, session):
    for rq_element in qbxml_msgs:
        request_id = int(rq_element.get('requestID', '0'))
        qb_table_name = rq_element.tag.replace('Rq', '')
        add = rq_element[0] if len(rq_element) > 0 else None
        first_child = add[0] if len(add) > 0 else None
        if first_child is not None and first_child.tag == 'TxnID':
            old_qb_id = first_child.text
            mapping = TransactionMapping(
                request_id=request_id,
                qb_add_rq_name=qb_table_name,
                is_trx_line_id=False,
                old_qb_id=old_qb_id
            )
            session.add(mapping)
            first_child.getparent().remove(first_child)
        else:
            pass

        add_journal_line_to_db(add, request_id, qb_table_name, session)

        add_line_ret_to_db(add, request_id, qb_table_name, session)


    session.commit()

def remove_empty_query_responses(root):
    # Find all elements with the specific statusMessage
    elements_to_remove = root.xpath(
        '//*[@statusMessage="A query request did not find a matching object in QuickBooks"]'
    )

    for elem in elements_to_remove:
        parent = elem.getparent()
        if parent is not None:
            parent.remove(elem)

    # Return the modified root element
    return root


def remove_unwanted_tags(root, tags_to_remove):
    for tag in tags_to_remove:
        if '/*' in tag:
            # Handle wildcard and paths like 'AccountRet/*FullName'
            parent_tag, child_wildcard = tag.split('/*')
            for parent in root.findall(f".//{parent_tag}"):
                for element in parent.findall(f".//*"):
                    if element.tag.endswith(child_wildcard):
                        parent.remove(element)
        elif '*' in tag:
            # Handle global wildcard like '*MyFullName'
            wildcard_tag = tag.replace('*', '')
            for element in root.findall(".//*"):
                if element.tag.endswith(wildcard_tag):
                    parent = element.getparent()
                    if parent is not None:
                        parent.remove(element)
        else:
            # Exact match for the tag without wildcards
            for element in root.xpath(f"//{tag}"):
                parent = element.getparent()
                if parent is not None:
                    parent.remove(element)
    return root


def create_data_ext_mod_rq(data_ext_ret, parent_id_macro, request_counter, table_name, line_macro=None):
    # Prepare DataExtAdd element
    data_ext_add_rq = ET.Element("DataExtAddRq", requestID=str(request_counter))
    data_ext_add = ET.Element("DataExtAdd")

    # Extract existing OwnerID
    owner_id_element = data_ext_ret.find("OwnerID")
    if owner_id_element is not None:
        owner_id = ET.Element("OwnerID")
        owner_id.text = owner_id_element.text
        data_ext_add.append(owner_id)
    else:
        pass

    # Extract existing DataExtName
    data_ext_name = data_ext_ret.find("DataExtName")
    if data_ext_name is not None:
        name_elem = ET.Element("DataExtName")
        name_elem.text = data_ext_name.text
        data_ext_add.append(name_elem)
    else:
        pass

    txn_data_ext_type = ET.Element("TxnDataExtType")
    txn_data_ext_type.text = table_name
    data_ext_add.append(txn_data_ext_type)

    txn_obj_ref = ET.Element("TxnID", useMacro=parent_id_macro)
    txn_obj_ref.text = parent_id_macro.split(':')[1]
    data_ext_add.append(txn_obj_ref)

    if line_macro is not None:
        txn_line_id_element = ET.Element("TxnLineID")
        txn_line_id_element.text = line_macro
        txn_line_id_element.set('useMacro', line_macro)
        data_ext_add.append(txn_line_id_element)
    else:
        pass

    # Extract existing DataExtValue
    data_ext_value = data_ext_ret.find("DataExtValue")
    if data_ext_value is not None:
        value_elem = ET.Element("DataExtValue")
        value_elem.text = data_ext_value.text
        data_ext_add.append(value_elem)
    else:
        pass

    data_ext_add_rq.append(data_ext_add)
    return data_ext_add_rq


def remove_tags(root):

    general_tags_to_remove = ['TimeCreated', 'TimeModified', 'EditSequence', 'TxnNumber',
                              'Sublevel', 'CustomerRet/*AddressBlock']
    root = remove_unwanted_tags(root, general_tags_to_remove)
    specific_tags_to_remove = ['AccountRet/FullName', 'AccountRet/Sublevel', 'AccountRet/Balance',
                           'AccountRet/TotalBalance', 'AccountRet/CashFlowClassification',
                               'AccountRet/SpecialAccountType', 'ClassRet/FullName', 'CustomerRet/FullName',
                               'CustomerRet/Balance', 'CustomerRet/TotalBalance']
    root = remove_unwanted_tags(root, specific_tags_to_remove)
    return root

def handle_data_ext(new_qbxml_msgs, data_ext_elements, add_rq, base_name, parent_request_id_for_data_ext, request_counter):

    add = add_rq[0]
    trx_def_macro = f'TxnID:{parent_request_id_for_data_ext}'
    add.set('defMacro', trx_def_macro)
    new_qbxml_msgs.append(add_rq)
    for data_ext_element in data_ext_elements:
        data_ext_element_parent = data_ext_element.getparent()
        if data_ext_element_parent == add:
            data_ext_add_rq = create_data_ext_mod_rq(data_ext_element, trx_def_macro, request_counter, base_name)
            request_counter += 1
            try:
                new_qbxml_msgs.append(data_ext_add_rq)
            except:
                new_qbxml_msgs.append(data_ext_add_rq)
        else:
            line_number = data_ext_element_parent[0].text.split('-')[0]
            line_macro = f'TxnLineID:{(parent_request_id_for_data_ext)}-{line_number}'
            data_ext_element_parent.set('defMacro', line_macro)
            data_ext_add_rq = create_data_ext_mod_rq(data_ext_element, trx_def_macro, parent_request_id_for_data_ext,
                                                     base_name, line_macro=line_macro)
            request_counter += 1
            try:
                new_qbxml_msgs.append(data_ext_add_rq)
            except:
                new_qbxml_msgs.append(data_ext_add_rq)
        try:
            data_ext_element_parent.remove(data_ext_element)
        except Exception as e:
            print(e)
            data_ext_element_parent.remove(data_ext_element)
            print('did it!')

    return new_qbxml_msgs, request_counter

def convert_ret_to_add(qbxml_msgs):
    request_counter = 1
    new_qbxml_msgs = ET.Element("QBXMLMsgsRq", onError="stopOnError")
    query_rs_list = qbxml_msgs.getchildren()
    for query_rs in query_rs_list:
        ret_list = query_rs.getchildren()
        for ret_element in ret_list:
            if ret_element.tag[-3:] == 'Ret':
                # Modify Ret tag to Add tag (e.g., CustomerRet -> CustomerAdd)
                base_name = ret_element.tag[:-3]
                ret_element.tag = f"{base_name}Add"
                add_rq = ET.Element(f"{base_name}AddRq", requestID=str(request_counter))
                parent_request_id_for_data_ext = request_counter
                request_counter += 1
                add_rq.append(ret_element)
                data_ext_elements = ret_element.xpath('.//DataExtRet')
                if data_ext_elements is not None:
                    new_qbxml_msgs, request_counter = handle_data_ext(new_qbxml_msgs, data_ext_elements, add_rq, base_name, parent_request_id_for_data_ext, request_counter)
                else:
                    try:
                        new_qbxml_msgs.append(add_rq)
                    except:
                        new_qbxml_msgs.append(add_rq)
            else:
                pass
    return new_qbxml_msgs


def process_response_xml(response_file_path, session):

    # Parse the XML response file
    parser = ET.XMLParser(remove_blank_text=True)
    tree = ET.parse(response_file_path, parser)
    root = tree.getroot()

    # Navigate to QBXMLMsgsRs element
    qbxml_msgs_rs = root.find('.//QBXMLMsgsRs')
    errors_requests = []

    for query_rs in qbxml_msgs_rs:
        request_id = int(query_rs.get('requestID', '0'))
        status_code = query_rs.get('statusCode')
        if status_code != '0':
            errors_requests.append(request_id)
        else:
            # Get the Ret element name (e.g., JournalEntryRet)
            for ret_element in query_rs:
                if ret_element.tag.endswith('Ret') and ret_element[0].tag == 'TxnID':
                    txn_id_element = ret_element[0]
                    if txn_id_element is not None:
                        new_qb_id = txn_id_element.text
                        ret_tag = ret_element.tag  # e.g., JournalEntryRet
                        # Map Ret tag to corresponding Add tag
                        qb_add_rq_name = ret_tag.replace('Ret', 'Add')

                        # Query the database for matching record
                        mapping = session.query(TransactionMapping).filter_by(
                            request_id=request_id,
                            qb_add_rq_name=qb_add_rq_name
                        ).first()

                        if mapping:
                            mapping.new_qb_id = new_qb_id
                            session.commit()
                        else:
                            print(f"No matching record found for request_id {request_id}, qb_add_rq_name {qb_add_rq_name}")
                    else:
                        pass
                    line_mappings = session.query(TransactionMapping).filter_by(
                        request_id=request_id,
                        qb_add_rq_name=qb_add_rq_name,
                        is_trx_line_id=True
                    ).all()
                    response_line_elements = [elem for elem in ret_element if elem.tag.endswith('Line')]
                    if len(line_mappings) == len(response_line_elements):
                        for mapping, line_elem in zip(line_mappings, response_line_elements):
                            txn_line_id_elem = line_elem.find('TxnLineID')
                            if txn_line_id_elem is not None:
                                mapping.new_qb_id = txn_line_id_elem.text
                            else:
                                print(f"No TxnLineID found in line element at sequence {mapping.line_sequence}")
                            session.commit()
                    else:
                        raise

                else:
                    pass

    # Close the session
    session.close()
    print(f'errors_requests: {errors_requests}')











