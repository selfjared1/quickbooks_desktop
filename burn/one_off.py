import lxml as et
from src.quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
import os

def save_xml_to_file(xml_string, file_path):
    # Write the XML string to the specified file path
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(xml_string)

def get_data(table_name):
    qb = QuickbooksDesktop()
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="13.0"?>
<QBXML>
    <QBXMLMsgsRq onError="stopOnError">
        <{table_name}QueryRq requestID="1">
        <RefNumber>00210203</RefNumber>
        <IncludeLineItems>true</IncludeLineItems>
        <OwnerID>0</OwnerID>
        </{table_name}QueryRq>
    </QBXMLMsgsRq>
</QBXML>"""
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    qb.begin_session()
    response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
    qb.close_qb()
    # Specify the desired file name and path
    file_name = f"{table_name}.xml"
    dir_path = os.path.join(os.path.expanduser("~"), r"Documents/QBW/New American Rotary Tools/xml data")  # e.g., save to the Documents folder
    file_path = os.path.join(dir_path, file_name)

    # Ensure the directory exists
    os.makedirs(dir_path, exist_ok=True)

    # Save the XML to the specified file
    save_xml_to_file(response, file_path)

    print(f"XML saved in file: {file_path}")


def add(table_name):
    qb = QuickbooksDesktop()
    xml_str = f"""<?xml version="1.0" encoding="utf-8"?><?qbxml version="15.0"?>
    <QBXML>
        <QBXMLMsgsRq onError="stopOnError">
            <{table_name}AddRq requestID="1">
                <BillAdd>
                    <VendorRef>
                        <FullName>NSK America Corporation</FullName>
                    </VendorRef>
                    <VendorAddress>
                        <Addr1>NSK AMERICA CORPORATION</Addr1>
                        <Addr2>PO Box 2675</Addr2>
                        <City>CAROL STREAM</City>
                        <State>IL</State>
                        <PostalCode>60132-2675</PostalCode>
                    </VendorAddress>
                    <APAccountRef>
                        <FullName>Accounts Payable</FullName>
                    </APAccountRef>
                    <TxnDate>2024-09-18</TxnDate>
                    <DueDate>2024-10-18</DueDate>
                    <RefNumber>00210203</RefNumber>
                    <Memo>Received items (bill to follow) 279633612832</Memo>
                    <ItemLineAdd>
                        <ItemRef>
                            <FullName>RA-271E</FullName>
                        </ItemRef>
                        <InventorySiteRef>
                            <FullName>ARTCO Monrovia</FullName>
                        </InventorySiteRef>
                        <SerialNumber>D2462616</SerialNumber>
                        <Desc>RA-271E - </Desc>
                        <Quantity>1</Quantity>
                        <Cost>373.80</Cost>
                        <Amount>373.80</Amount>
                        <CustomerRef>
                            <FullName>Freedom Tool Supply</FullName>
                        </CustomerRef>
                        <BillableStatus>HasBeenBilled</BillableStatus>
                        </ItemLineAdd>
                    <ItemLineAdd>

                        <ItemRef>
                        <FullName>Tool Holding:90525</FullName>
                        </ItemRef>
                        <InventorySiteRef>
                            <FullName>Drop Ship</FullName>
                        </InventorySiteRef>
                        <Desc>CHS Collet - 2.5mm</Desc>
                        <Quantity>3</Quantity>
                        <Cost>39.31</Cost>
                        <Amount>117.94</Amount>
                        <CustomerRef>

                        <FullName>Freedom Tool Supply</FullName>
                        </CustomerRef>

                    </ItemLineAdd>
                </BillAdd>
            </{table_name}AddRq>
        </QBXMLMsgsRq>
    </QBXML>"""
    qb.qbXMLRP = qb.dispatch()
    qb.open_connection()
    qb.begin_session()
    response = ''
    try:
        response = qb.qbXMLRP.ProcessRequest(qb.ticket, xml_str)
    except Exception as e:
        print(e)
    qb.close_qb()
    print(response)


if __name__ == '__main__':
    # get_data('Bill')
    add('Bill')
