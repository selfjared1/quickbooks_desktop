from core.session_manager import SessionManager
from lxml import etree as et
import pandas as pd

class QuickBooksDesktop(SessionManager):
    """
    To do everything in QBD

    """
    def __init__(self):
        self.lists_dict = {
            'accounts': ('AccountQueryRq', '/QBXML/QBXMLMsgsRs/AccountQueryRs/AccountRet'),
        }

    def get_list(self, list_name):
        root = et.Element(self.lists_dict[list_name.lower()][0])
        qb = SessionManager()
        response = qb.send_xml(root)
        df = pd.read_xml(response, self.lists_dict[list_name][1])
        return df

if __name__ == '__main__':
    qb = QuickBooksDesktop()
    df = qb.get_list('accounts')
    print(df)
