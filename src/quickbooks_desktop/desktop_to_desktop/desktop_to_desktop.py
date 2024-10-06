
import os
import lxml.etree as ET
from src.quickbooks_desktop.desktop_to_desktop.query_all import query_all
from burn.phone_notifications import notify_jared_process_is_done

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

def get_data(response_file_path):
    query_all(response_file_path)
    notify_jared_process_is_done()


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



def get_query_rs_list(source_file_path):
    # Load the source XML data
    tree = ET.parse(source_file_path)
    root = tree.getroot()
    return root

def add_defmacro_for_ids(root):
    # Loop through both TxnID and ListID
    id_to_adjust = ['TxnID']
    # id_to_adjust = ['TxnID', 'ListID']
    for id_type in id_to_adjust:
        # Find all elements that have a TxnID or ListID child and their tag ends with 'Ret'
        for id_element in root.xpath(f"//*[contains(local-name(), 'Ret')]/*[local-name()='{id_type}']"):
            parent_element = id_element.getparent()

            # Get the ID value (either TxnID or ListID)
            id_value = id_element.text

            if id_value:
                # Add to defMacro attribute in the parent element
                # If defMacro already exists, append the new value
                current_defmacro = parent_element.get('defMacro', '')
                if current_defmacro:
                    parent_element.set('defMacro', f'{current_defmacro}, {id_type}:{id_value}')
                else:
                    parent_element.set('defMacro', f'{id_type}:{id_value}')

            # Remove the TxnID or ListID element
            parent_element.remove(id_element)

    return root

#specific things to do:
def elevate_tax_line_id(root):
    for tax_line_info in root.findall(".//AccountRet/TaxLineInfoRet"):
        tax_line_id = tax_line_info.find("TaxLineID")

        if tax_line_id is not None:
            parent = tax_line_info.getparent()
            parent.append(tax_line_id)

        if parent is not None:
            parent.remove(tax_line_info)

    return root


def add_data_ext_add(new_qbxml_msgs, data_ext_rets, parent_id_macro, request_counter):
    created_count = 0  # Track how many DataExtAdd elements were created

    # Loop through each DataExtRet that was passed
    for data_ext_ret in data_ext_rets:
        # Prepare DataExtAdd element
        data_ext_add_rq = ET.Element("DataExtAddRq", requestID=str(request_counter))
        data_ext_add = ET.Element("DataExtAdd")

        # Extract existing OwnerID
        owner_id_element = data_ext_ret.find("OwnerID")
        if owner_id_element is not None:
            owner_id = ET.Element("OwnerID")
            owner_id.text = owner_id_element.text
            data_ext_add.append(owner_id)

        # Extract existing DataExtName
        data_ext_name = data_ext_ret.find("DataExtName")
        if data_ext_name is not None:
            name_elem = ET.Element("DataExtName")
            name_elem.text = data_ext_name.text
            data_ext_add.append(name_elem)

        # Extract existing DataExtType (if applicable)
        data_ext_type = data_ext_ret.find("DataExtType")
        if data_ext_type is not None:
            type_elem = ET.Element("DataExtType")
            type_elem.text = data_ext_type.text
            data_ext_add.append(type_elem)

        # Extract existing DataExtValue
        data_ext_value = data_ext_ret.find("DataExtValue")
        if data_ext_value is not None:
            value_elem = ET.Element("DataExtValue")
            value_elem.text = data_ext_value.text
            data_ext_add.append(value_elem)

        # Add ListDataExtType or TxnDataExtType depending on whether it's ListID or TxnID
        if "ListID" in parent_id_macro:
            list_data_ext_type = ET.Element("ListDataExtType")
            list_data_ext_type.text = "Customer"  # Adjust dynamically if needed
            data_ext_add.append(list_data_ext_type)

            list_obj_ref = ET.Element("ListObjRef")
            list_id = ET.Element("ListID", useMacro=parent_id_macro)
            list_obj_ref.append(list_id)
            data_ext_add.append(list_obj_ref)

        elif "TxnID" in parent_id_macro:
            txn_data_ext_type = ET.Element("TxnDataExtType")
            txn_data_ext_type.text = "Invoice"  # Adjust dynamically if needed
            data_ext_add.append(txn_data_ext_type)

            txn_obj_ref = ET.Element("TxnID", useMacro=parent_id_macro)
            data_ext_add.append(txn_obj_ref)

        # Append the DataExtAdd element to DataExtAddRq, and increment the request_counter
        data_ext_add_rq.append(data_ext_add)
        new_qbxml_msgs.append(data_ext_add_rq)
        created_count += 1
        request_counter += 1  # Increment the request_counter for each DataExtAdd

    return created_count, request_counter


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


def transform_qbxml(root):
    add_defmacro_for_ids(root)
    root = remove_tags(root)
    root = elevate_tax_line_id(root)

    # Locate QBXMLMsgsRs and convert it to QBXMLMsgsRq
    qbxml_msgs = root.find("QBXMLMsgsRs")
    qbxml_msgs.tag = "QBXMLMsgsRq"
    qbxml_msgs.set("onError", "stopOnError")

    # Create a new QBXMLMsgsRq to hold the modified data
    new_qbxml_msgs = ET.Element("QBXMLMsgsRq", onError="stopOnError")

    request_counter = 1

    # Loop through all QueryRs elements and their children
    for query_rs in qbxml_msgs.getchildren():
        for ret_element in query_rs.getchildren():
            if ret_element.tag[-3:] == 'Ret':
                # Modify Ret tag to Add tag (e.g., CustomerRet -> CustomerAdd)
                base_name = ret_element.tag[:-3]
                ret_element.tag = f"{base_name}Add"

                # Find first child (ListID or TxnID) for macro use
                first_child = ret_element.getchildren()[0]
                if first_child.tag == "ListID":
                    parent_id_macro = f"ListID:{first_child.text}"
                elif first_child.tag == "TxnID":
                    parent_id_macro = f"TxnID:{first_child.text}"
                else:
                    parent_id_macro = ""

                # Separate DataExtRet elements before modifying the Ret element
                data_ext_rets = ret_element.findall(".//DataExtRet")
                if data_ext_rets:
                    # Remove DataExtRet from ret_element
                    for data_ext_ret in data_ext_rets:
                        try:
                            if data_ext_ret in data_ext_rets:
                                ret_element.remove(data_ext_ret)
                            else:
                                raise
                        except Exception as e:
                            print(e)
                else:
                    pass

                # Create and append the AddRq (e.g., CustomerAddRq)
                add_rq = ET.Element(f"{base_name}AddRq", requestID=str(request_counter))
                request_counter += 1
                add_rq.append(ret_element)
                new_qbxml_msgs.append(add_rq)

                # Handle DataExtRet elements (create DataExtAddRq)
                if parent_id_macro and data_ext_rets:
                    count, request_counter = add_data_ext_add(new_qbxml_msgs, data_ext_rets, parent_id_macro, request_counter)
                    print(f"Added {count} DataExtAddRq elements")
                else:
                    pass

    # Replace the original QBXMLMsgsRs with the new modified QBXMLMsgsRq
    root.replace(qbxml_msgs, new_qbxml_msgs)

    # Optionally remove unwanted tags
    last_tags_to_remove = ['ListID']
    root = remove_unwanted_tags(root, last_tags_to_remove)

    return root



if __name__ == '__main__':
    #todo: add_defmacro_for_ids make sure to uncomment so ListID gets a macro too
    #todo: in .... change general_tags_to_remove to not have ListID



    file_location = os.path.expanduser("~/Desktop/burn")
    response_file_path = os.path.join(file_location, f"actual_full_file.xml")
    get_data(response_file_path)

    # root = get_query_rs_list(response_file_path)
    # root = transform_qbxml(root)
    #
    # xml_string = ET.tostring(root, pretty_print=True, xml_declaration=False, encoding="UTF-8").decode()
    # full_xml = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?> {xml_string}"""
    # # Write the string to a file
    # add_request_file_path = os.path.join(file_location, fr"C:\Users\JaredSelf\PycharmProjects\quickbooks_desktop\burn\add_request.xml")
    # with open(add_request_file_path, 'w', encoding='utf-8') as file:
    #     file.write(full_xml)







