import os
from lxml import etree
import easygui
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop


# Step 1: Get data from QuickBooks and save it
def get_data_from_quickbooks(data_transfer_dict, file_location, qb):
    for table_name, config in data_transfer_dict.items():
        included_str = ''
        if 'active_status' in config.keys() and config['active_status']:
            included_str += "<ActiveStatus>All</ActiveStatus>"
        else:
            pass

        if 'include_line_items' in config.keys() and config['include_line_items']:
            included_str += "<IncludeLineItems>true</IncludeLineItems>"
        else:
            pass



        xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
        <QBXML>
            <QBXMLMsgsRq onError="stopOnError">
                <{table_name}QueryRq requestID="1">
                <RefNumber>00210203</RefNumber>
                {included_str}
                <OwnerID>0</OwnerID>
                </{table_name}QueryRq>
            </QBXMLMsgsRq>
        </QBXML>"""

        # Send the request to QuickBooks and get the response
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)

        # Save the response XML to a file
        file_path = os.path.join(file_location, f"{table_name}.xml")
        with open(file_path, 'w') as file:
            file.write(response)

        print(f"{table_name}.xml saved at {file_path}")


# Step 2: Process saved data and create {table_name}Add.xml
def create_add_xml(data_transfer_dict, file_location):
    for table_name, config in data_transfer_dict.items():
        # Read the original {table_name}.xml file
        file_path = os.path.join(file_location, f"{table_name}.xml")
        parser = etree.XMLParser(remove_blank_text=True)

        try:
            tree = etree.parse(file_path, parser)
            root = tree.getroot()
        except Exception as e:
            print(f"Error reading {table_name}.xml: {e}")
            continue

        # Drill down to the "Ret" element (e.g., <AccountRet>)
        ret_elements = root.xpath(f"//{table_name}Ret")

        if not ret_elements:
            print(f"No {table_name}Ret elements found in {table_name}.xml")
            continue

        # Create the new root for the AddRq (e.g., <AccountAddRq>)
        new_root = etree.Element("QBXML")
        qbxml_msgs_rq = etree.SubElement(new_root, "QBXMLMsgsRq", onError="stopOnError")
        add_rq = etree.SubElement(qbxml_msgs_rq, f"{table_name}AddRq", requestID="1")

        # Process each Ret element
        for ret_elem in ret_elements:
            processed_xml = process_xml(ret_elem, config['unallowed_tags'], config['swap_tags'], table_name)

            # Add the processed element to the new AddRq structure
            add_rq.append(processed_xml)

        # Save the new XML file as {table_name}Add.xml
        add_file_path = os.path.join(file_location, f"{table_name}Add.xml")
        with open(add_file_path, 'wb') as add_file:
            add_file.write(etree.tostring(new_root, pretty_print=True, encoding="utf-8"))

        print(f"{table_name}Add.xml saved at {add_file_path}")


# Step 3: Send {table_name}Add.xml to QuickBooks and save the response
def send_add_xml_to_quickbooks(data_transfer_dict, file_location, qb):
    for table_name in data_transfer_dict.keys():
        add_file_path = os.path.join(file_location, f"{table_name}Add.xml")

        try:
            # Read the {table_name}Add.xml file
            with open(add_file_path, 'r') as add_file:
                add_xml_str = add_file.read()

            # Send the AddRq to QuickBooks
            response = qb.qbXMLRP.ProcessRequest(qb.ticket, add_xml_str)

            # Save the response to a file
            response_file_path = os.path.join(file_location, f"{table_name}Response.xml")
            with open(response_file_path, 'w') as response_file:
                response_file.write(response)

            print(f"Response from QuickBooks for {table_name} saved at {response_file_path}")

        except Exception as e:
            print(f"Error processing {table_name}Add.xml: {e}")


# Helper function to process the XML (removes unallowed tags and swaps tags)
def process_xml(xml_elem, unallowed_tags, swap_tags, table_name):
    # Remove unallowed tags
    for tag in unallowed_tags:
        for elem in xml_elem.xpath(f".//{tag}"):
            parent = elem.getparent()
            if parent is not None:
                parent.remove(elem)

    # Swap tags
    for swap in swap_tags:
        for old_tag, new_tag in swap.items():
            for elem in xml_elem.xpath(f".//{old_tag}"):
                elem.tag = new_tag

    # Change parent and child tags based on table_name (e.g., AccountRet -> AccountAdd)
    parent_tag = f"{table_name}Ret"
    child_tag = f"{table_name}Add"

    for parent_elem in xml_elem.xpath(f"//{parent_tag}"):
        new_child_elem = etree.Element(child_tag)  # Create new child element
        new_child_elem.extend(parent_elem)  # Move children of parent to new child
        parent_elem.getparent().replace(parent_elem, new_child_elem)  # Replace parent with new child

    return xml_elem





if __name__ == '__main__':
    pass_1_data_transfer_dict = [{
        'Account': {
            'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
            'swap_tags': [{"AccountRet": "AccountAddRq"}],
            'active_status': False,
        }
    }]

    file_location = "C:/path/to/save"
    qb = QuickbooksDesktop()

    # Step 1: Get data from QuickBooks and save it
    get_data_from_quickbooks(pass_1_data_transfer_dict, file_location, qb)

    # Step 2: Create {table_name}Add.xml from saved data
    create_add_xml(pass_1_data_transfer_dict, file_location)

    # Step 3: Send the {table_name}Add.xml data to QuickBooks
    send_add_xml_to_quickbooks(pass_1_data_transfer_dict, file_location, qb)

    # pass_1_data_transfer_dict = [{
    #     'Account': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"AccountRet": "AccountAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'BillingRate': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"BillingRateRet": "BillingRateAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'Class': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ClassRet": "ClassAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'Currency': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"CurrencyRet": "CurrencyAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'Customer': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"CustomerRet": "CustomerAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'CustomerMsg': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"CustomerMsgRet": "CustomerMsgAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'CustomerType': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"CustomerTypeRet": "CustomerTypeAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'DateDrivenTerms': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"DateDrivenTermsRet": "DateDrivenTermsAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'Employee': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"EmployeeRet": "EmployeeAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'InventorySite': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"InventorySiteRet": "InventorySiteAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemDiscount': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemDiscountRet": "ItemDiscountAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemFixedAsset': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemFixedAssetRet": "ItemFixedAssetAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemGroup': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemGroupRet": "ItemGroupAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemInventory': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemInventoryRet": "ItemInventoryAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemInventoryAssembly': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemInventoryAssemblyRet": "ItemInventoryAssemblyAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemNonInventory': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemNonInventoryRet": "ItemNonInventoryAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemOtherCharge': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemOtherChargeRet": "ItemOtherChargeAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemPayment': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemPaymentRet": "ItemPaymentAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemSalesTax': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemSalesTaxRet": "ItemSalesTaxAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemSalesTaxGroup': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemSalesTaxGroupRet": "ItemSalesTaxGroupAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ItemService': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ItemServiceRet": "ItemServiceAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'JobType': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"JobTypeRet": "JobTypeAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'OtherName': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"OtherNameRet": "OtherNameAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'PaymentMethod': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"PaymentMethodRet": "PaymentMethodAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'PriceLevel': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"PriceLevelRet": "PriceLevelAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'SalesRep': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"SalesRepRet": "SalesRepAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'SalesTaxCode': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"SalesTaxCodeRet": "SalesTaxCodeAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'ShipMethod': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"ShipMethodRet": "ShipMethodAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'StandardTerms': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"StandardTermsRet": "StandardTermsAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'UnitOfMeasureSet': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"UnitOfMeasureSetRet": "UnitOfMeasureSetAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'Vehicle': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"VehicleRet": "VehicleAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'Vendor': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"VendorRet": "VendorAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'VendorType': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"VendorTypeRet": "VendorTypeAddRq"}],
    #         'include_line_items': False,
    #     },
    #     'WorkersCompCode': {
    #         'unallowed_tags': ["ListID", "TimeCreated", "TimeModified"],
    #         'swap_tags': [{"WorkersCompCodeRet": "WorkersCompCodeAddRq"}],
    #         'include_line_items': False,
    #     }
    # }]