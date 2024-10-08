import lxml.etree as ET
from src.quickbooks_desktop.desktop_to_desktop.models import TransactionMapping, DataExtMod


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

def add_journal_line_to_db(add, request_id, qb_table_name, old_qb_trx_id, session):
    txn_line_id_elements = add.xpath('.//TxnLineID')
    for txn_line_id_elem in txn_line_id_elements:
        parent = txn_line_id_elem.getparent()
        if parent.tag in ['JournalCreditLine', 'JournalDebitLine']:
            old_qb_trx_line_id = txn_line_id_elem.text
            mapping = TransactionMapping(
                request_id=request_id,
                qb_add_rq_name=qb_table_name,
                old_qb_trx_id=old_qb_trx_id,
                old_qb_trx_line_id=old_qb_trx_line_id,
            )
            session.add(mapping)
            parent.remove(txn_line_id_elem)
        else:
            pass

def add_line_ret_to_db(add, request_id, qb_table_name, old_qb_trx_id, session):
    # txn_line_id_elements = add.xpath('.//TxnLineID')
    txn_line_ret_elements = add.xpath(
        ".//*[substring(local-name(), string-length(local-name()) - string-length('LineRet') + 1) = 'LineRet' or substring(local-name(), string-length(local-name()) - string-length('LineGroupRet') + 1) = 'LineGroupRet']"
    )

    for txn_line_ret in txn_line_ret_elements:
        if txn_line_ret[0].tag[-6:] == 'LineID':
            txn_line_id_elem = txn_line_ret[0]
            old_qb_trx_line_id = txn_line_id_elem.text
            mapping = TransactionMapping(
                request_id=request_id,
                qb_add_rq_name=qb_table_name,
                old_qb_trx_id=old_qb_trx_id,
                old_qb_trx_line_id=old_qb_trx_line_id,
            )
            session.add(mapping)
            txn_line_id_elem.getparent().remove(txn_line_id_elem)
        else:
            pass
        txn_line_ret.tag = txn_line_ret.tag.replace('Ret', 'Add')


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

def handle_data_ext(data_ext_elements, add_element, base_name, request_id, session, batch_size=1000):
    count = 0
    for data_ext_element in data_ext_elements:
        data_ext_element_parent = data_ext_element.getparent()
        if data_ext_element_parent == add_element:
            data_ext_mod = DataExtMod(
                request_id=request_id,
                owner_id=data_ext_element.find("OwnerID").text,
                data_ext_name=data_ext_element.find('DataExtName').text,
                txn_data_ext_type=base_name,
                txn_id_old=add_element.find('TxnID').text,
                data_ext_value=data_ext_element.find('DataExtValue').text,
            )
            session.add(data_ext_mod)
            count += 1
        else:
            if data_ext_element_parent[0].tag.endswith('LineID'):
                data_ext_mod = DataExtMod(
                    request_id=request_id,
                    owner_id=data_ext_element.find("OwnerID").text,
                    data_ext_name=data_ext_element.find('DataExtName').text,
                    txn_data_ext_type=base_name,
                    txn_id_old=add_element.find('TxnID').text,
                    txn_line_id_old=data_ext_element_parent[0].text,
                    data_ext_value=data_ext_element.find('DataExtValue').text,
                )
                session.add(data_ext_mod)
                count += 1
            else:
                try:
                    print('program drops from here sometimes')
                except Exception as e:
                    pass
        if count >= batch_size:
            print('batch 1000')
            session.commit()
            count = 0
    if count > 0:
        session.commit()


def convert_ret_to_add(qbxml_msgs, session):
    request_counter = 1
    new_qbxml_msgs = ET.Element("QBXMLMsgsRq", onError="stopOnError")
    query_rs_list = qbxml_msgs.getchildren()
    for i in range(len(query_rs_list)):
        query_rs = query_rs_list[i]
        ret_list = query_rs.getchildren()
        for i in range(len(ret_list)):
            ret_element = ret_list[i]
            if ret_element.tag.endswith('Ret'):
                base_name = ret_element.tag[:-3]
                ret_element.tag = f"{base_name}Add"
                request_id = str(request_counter)
                add_rq = ET.Element(f"{base_name}AddRq", requestID=request_id)
                request_counter += 1
                add_rq.append(ret_element)
                new_qbxml_msgs.append(add_rq)
                data_ext_elements = ret_element.findall('.//DataExtRet')
                if data_ext_elements:
                    handle_data_ext(data_ext_elements, ret_element, base_name, request_id, session)
                    # print('finished handle_data_ext')
                else:
                    pass
            else:
                pass
    print('exited loop')
    data_ext_elements = ret_element.xpath('.//DataExtRet')
    for data_ext_element in data_ext_elements:
        parent = data_ext_element.getparent()
        parent.remove(data_ext_element)
    return new_qbxml_msgs

def add_trx_id_to_trx_mapping_table(new_qb_trx_id, request_id, qb_add_rq_name, session):
    # Query the database for matching record
    trx_id_mappings = session.query(TransactionMapping).filter(
        TransactionMapping.request_id == request_id,
        TransactionMapping.qb_add_rq_name == qb_add_rq_name
    ).all()

    if trx_id_mappings:
        for trx_id_mapping in trx_id_mappings:
            trx_id_mapping.new_qb_trx_id = new_qb_trx_id
        session.commit()
    else:
        print(f"No matching record found for request_id {request_id}, qb_add_rq_name {qb_add_rq_name}")

def add_trx_line_id_to_trx_mapping_table(request_id, add_rq_name, response_line_elements, session):
    line_mappings = session.query(TransactionMapping).filter(
        TransactionMapping.request_id == request_id,
        TransactionMapping.qb_add_rq_name == add_rq_name,
        TransactionMapping.old_qb_trx_line_id.is_not(None)
    ).all()

    if len(line_mappings) == len(response_line_elements):
        for mapping, line_elem in zip(line_mappings, response_line_elements):
            txn_line_id_elem = line_elem.find('TxnLineID')
            if txn_line_id_elem is not None:
                mapping.new_qb_trx_line_id = txn_line_id_elem.text
            else:
                print(
                    f"No TxnLineID found in line element at sequence {mapping.request_id} for {mapping.qb_add_rq_name}")
        session.commit()
    else:
        raise NotImplementedError("This isn't coded yet")


def add_trx_id_to_data_ext_mod_table(new_qb_trx_id, request_id, qb_add_rq_name, session):
    data_ext_mods = session.query(DataExtMod).filter(
        DataExtMod.request_id == request_id,
        DataExtMod.txn_data_ext_type == qb_add_rq_name.replace('Add', '')
    ).all()

    if data_ext_mods:
        for data_ext_mod in data_ext_mods:
            data_ext_mod.txn_id_new = new_qb_trx_id
        session.commit()
    else:
        print(
            f"No matching record found for request_id {request_id}, qb_add_rq_name {qb_add_rq_name}")


def add_trx_line_id_to_data_ext_mod_table(request_id, add_rq_name, response_line_elements, session):
    for response_line_element in response_line_elements:
        data_ext_mods_with_line_ids = session.query(DataExtMod).filter(
            DataExtMod.request_id == request_id,
            DataExtMod.txn_data_ext_type == add_rq_name.replace('Add', ''),
            DataExtMod.txn_line_id_old._is(response_line_element.find('TxnLineID').text)
        ).all()
        for data_ext_mod in data_ext_mods_with_line_ids:
            data_ext_mod.txn_line_id_new = response_line_element.find('TxnLineID').text
        session.commit()


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
                    qb_add_rq_name = ret_element.tag.replace('Ret', 'Add')
                    if txn_id_element is not None:
                        new_qb_trx_id = txn_id_element.text
                        add_trx_id_to_trx_mapping_table(new_qb_trx_id, request_id, qb_add_rq_name, session)
                        add_trx_id_to_data_ext_mod_table(new_qb_trx_id, request_id, qb_add_rq_name, session)

                    else:
                        pass

                    response_line_elements = [elem for elem in ret_element if elem.tag.endswith('LineRet')]
                    add_trx_line_id_to_trx_mapping_table(request_id, qb_add_rq_name, response_line_elements, session)
                    add_trx_line_id_to_data_ext_mod_table(request_id, qb_add_rq_name, response_line_elements, session)
                else:
                    pass

    # Close the session
    session.close()
    print(f'errors_requests: {errors_requests}')

def reorder_xml_in_entire_document(entire_xml, parent_to_loop_through, out_of_place_tag, tag_before, tag_after):
    """
    Reorder child elements within each occurrence of parent_to_loop_through in the entire XML.

    For each occurrence of out_of_place_tag within parent_element,
    move it to be after tag_before, or before tag_after if tag_before is not found.

    :param entire_xml: The root element of the entire XML document.
    :param parent_to_loop_through: The tag name of the parent elements to process.
    :param out_of_place_tag: The tag name of the element to be repositioned.
    :param tag_before: The tag name of the element after which out_of_place_tag should be placed.
    :param tag_after: The tag name of the element before which out_of_place_tag should be placed if tag_before is not found.
    """
    # Find all parent elements in the entire XML
    parent_elements = entire_xml.findall('.//' + parent_to_loop_through)

    for parent_element in parent_elements:
        # Collect all child elements
        children = list(parent_element)

        # Extract out_of_place_tag elements and their original positions
        elements_to_move = []
        indices_to_remove = []
        for i, child in enumerate(children):
            if child.tag == out_of_place_tag:
                elements_to_move.append(child)
                indices_to_remove.append(i)
            else:
                pass

        # Remove out_of_place_tag elements from children list
        for index in sorted(indices_to_remove, reverse=True):
            del children[index]

        # Find index of tag_before
        try:
            index_tag_before = next(i for i, child in enumerate(children) if child.tag == tag_before)
            # Insert elements after tag_before
            insertion_index = index_tag_before + 1
            for elem in elements_to_move:
                children.insert(insertion_index, elem)
                insertion_index += 1  # Increment to maintain order
        except StopIteration:
            # tag_before not found, look for tag_after
            try:
                index_tag_after = next(i for i, child in enumerate(children) if child.tag == tag_after)
                # Insert elements before tag_after
                insertion_index = index_tag_after
                for elem in elements_to_move:
                    children.insert(insertion_index, elem)
                    insertion_index += 1
            except StopIteration:
                # Neither tag_before nor tag_after found, append elements at the end
                children.extend(elements_to_move)

        # Remove all existing children from parent_element
        parent_element.clear()

        # Append children back to parent_element in the new order
        for child in children:
            parent_element.append(child)

def remove_amount_if_qty_and_rate(root):
    """
        Removes the <Amount> tag from line items that have both <Quantity> and <Rate>.

        :param root: The root element of the XML tree.
        :return: The modified root element.
        """
    # Find all line elements
    # Assuming line elements are those where the tag ends with 'LineRet'
    line_elements = root.xpath(".//*[substring(name(), string-length(name()) - 6) = 'LineRet']")

    # Loop through each line element
    for line in line_elements:
        # Check if the line has both Quantity and Rate tags
        quantity = line.find('Quantity')
        rate = line.find('Rate')
        if quantity is not None and rate is not None:
            # Remove the Amount tag if it exists
            amount = line.find('Amount')
            if amount is not None:
                parent = amount.getparent()
                parent.remove(amount)
    return root


def remove_amount_from_subtotals(root, item_names):
    """
    Removes the <Amount> tag from parent elements of <ItemRef><FullName> that match any name in item_names.

    :param root: The root element of the XML tree.
    :param item_names: A list of strings representing the FullName values to search for.
    :return: The modified root element.
    """
    # Iterate over each item name
    for item_name in item_names:
        # Find all <FullName> elements under <ItemRef> with text equal to item_name
        full_name_elements = root.xpath(f".//ItemRef[FullName='{item_name}']/FullName")

        # Iterate over each matching <FullName> element
        for full_name in full_name_elements:
            # Get the parent <ItemRef> element
            item_ref = full_name.getparent()
            if item_ref is not None:
                # Get the parent of <ItemRef>, which is assumed to be the line element
                line_element = item_ref.getparent()
                if line_element is not None:
                    # Find the <Amount> element within the line element
                    amount = line_element.find('Amount')
                    if amount is not None:
                        # Remove the <Amount> element from its parent
                        line_element.remove(amount)
    return root

def truncate_tag_text(xml_root, tag_name, max_length):

    for elem in xml_root.findall(f'.//{tag_name}'):
        if elem.text and len(elem.text) > max_length:
            elem.text = elem.text[:max_length]
        else:
            pass
    return xml_root


def remove_uncle_tag_based_on_xpath(root, search_xpath, uncle_to_remove):
    """This is mainly looking for sales tax items and removing the Rate which is a uncle"""
    # Find all elements matching the search_xpath
    matching_elements = root.xpath(search_xpath)

    for elem in matching_elements:
        # Check if the element's text matches the target value
        parent = elem.getparent()
        grandparent = parent.getparent()
        tag_element = grandparent.find(uncle_to_remove)
        if tag_element is not None:
            # Remove the tag_to_remove element from the grandparent
            grandparent.remove(tag_element)
        else:
            pass
    return root
