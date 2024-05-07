from core.session_manager import SessionManager
from lxml import etree as et
import sqlite3
from utility.utilities import remove_query_from_string

class QuickBooksDesktop(SessionManager):

    def __init__(self):
        super(QuickBooksDesktop).__init__()


    def parse_response_xml(self, table_name, response):
        """"
        table_query: an example is 'AccountQuery' as a string
        """
        table_name = remove_query_from_string(table_name)
        xpath = f'''/QBXML/QBXMLMsgsRs/{table_name}QueryRs/{table_name}Ret'''
        tree = et.fromstring(response)
        tree = tree.xpath(xpath)
        list_of_instances = []
        for element in tree:
            MyClass = eval(table_name)
            list_of_instances += [MyClass.from_xml(element)]
        return list_of_instances

    def get_table(self, table_name):
        if 'Query' in table_name:
            table_name = table_name.replace('Query', '')
        else:
            pass
        root = et.Element(table_name + 'QueryRq')
        qb = SessionManager()
        response = qb.send_xml(root)
        list_of_instances = self.parse_response_xml(table_name, response)
        return list_of_instances


    def replicate(self):
        connection = sqlite3.connect('qb_data.db')
        for code in self.query.keys():
            df = self.get_table(self.query[code])
            if df is not None:
                df.to_sql(code, connection, if_exists='replace', index=False)

    # def generate_xml_files(self):
    #     for table_name in self.query.keys():
    #         print(f'begin {table_name}')
    #         root = et.Element(table_name + 'Rq')
    #         qb = SessionManager()
    #         response = qb.send_xml(root)
    #         try:
    #             with open(f"{table_name}.xml", "wb") as xml_writer:
    #                 xml_writer.write(response)
    #         except IOError:
    #             pass

