
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
    # Loop through all tags in the XML and remove the unwanted ones
    for tag in tags_to_remove:
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

def write_xml_to_file(root, file_path):
    # Convert the root to a string
    xml_string = ET.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()

    # Write the string to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(xml_string)

def transform_qbxml(root):
    tags_to_remove = ['ListID', 'TimeCreated', 'TimeModified', 'EditSequence', 'TxnNumber']
    root = remove_unwanted_tags(root, tags_to_remove)

    # Find and update QBXMLMsgsRs to QBXMLMsgsRq
    qbxml_msgs = root.find("QBXMLMsgsRs")
    qbxml_msgs.tag = "QBXMLMsgsRq"
    qbxml_msgs.set("onError", "stopOnError")
    request_counter = 1  # Initialize the requestID counter

    # Elevate all Ret elements up one level and remove QueryRs elements
    for query_rs in qbxml_msgs.getchildren():
        # Move all Ret elements (e.g., PurchaseOrderRet) to be direct children of QBXMLMsgsRq
        for ret_element in query_rs.getchildren():
            qbxml_msgs.append(ret_element)
        qbxml_msgs.remove(query_rs)

    # Now iterate over each Ret element and wrap it with AddRq
    for ret_element in qbxml_msgs.getchildren():
        # Extract the base table name (e.g., from PurchaseOrderRet to PurchaseOrder)
        if ret_element.tag[:-3] == 'Ret':
            base_name = ret_element.tag[:-3]  # Remove 'Ret' from tag name
            ret_element.tag = f"{base_name}Add"
            add_rq = ET.Element(f"{base_name}AddRq", requestID=str(request_counter))
            request_counter += 1
            add_rq.append(ret_element)
            qbxml_msgs.replace(ret_element, add_rq)
        else:
            pass
    return root



if __name__ == '__main__':
    file_location = os.path.expanduser("~/Desktop/burn")
    response_file_path = os.path.join(file_location, f"full_file.xml")
    # get_data(response_file_path)

    root = get_query_rs_list(response_file_path)
    root = transform_qbxml(root)

    with open(response_file_path, 'w') as response_file:
        response_file.write(response)





