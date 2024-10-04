import lxml as et
from quickbooks_desktop.quickbooks_desktop import QuickbooksDesktop
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


if __name__ == '__main__':
    get_data('Customer')

