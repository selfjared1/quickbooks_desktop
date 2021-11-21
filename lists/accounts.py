from lxml import etree as et
from core.session_manager import SessionManager
from core.processing_xml import XML2DataFrame

class Account():
    def __init__(self, account_xml=None, **kwargs):
        self.xml = account_xml
        self.id = None
        self.time_created = None
        self.time_last_modified = None
        self.edit_sequence = None
        self.name = None
        self.full_name = None
        self.is_active = None
        self.parent_id = None
        self.parent_full_name = None
        self.sublevel = None
        self.account_type = None
        self.special_account_type = None
        self.account_number = None
        self.bank_number = None
        self.desc = None
        self.balance = None
        self.total_balance = None
        self.tax_line_id = None
        self.tax_line_name = None
        self.tax_line_info_ret = None
        self.cash_flow_classification = None
        self.currency_id = None
        self.currency_full_name = None
        self.data_extension_owner_id = None
        self.data_extension_type = None
        self.data_extension_value = None
        self.parse_account_xml()

    def get_parent_full_name(self):
        if not self.xml.xpath('//ParentRef'):
            # todo: check the xml path below
            print(self.xml.xpath('//ParentRef//ListID').text)
            print(self.xml.xpath('//ParentRef//FullName').text)
            self.parent_id = None #todo: replace with xpath
            self.parent_full_name = None #todo: replace with xpath

    def get_tax_line(self):
        # todo: make below work
        self.tax_line_id = self.xml.find('ListID').text
        self.tax_line_name = self.xml.find('ListID').text
        self.tax_line_info_ret = self.xml.find('ListID').text

    def get_currency(self):
        # todo: make below work
        self.currency_id = self.xml.find('ListID').text
        self.currency_full_name = self.xml.find('ListID').text

    def get_data_extension(self):
        # todo: make below work
        self.data_extension_owner_id = self.xml.find('ListID').text
        self.data_extension_type = self.xml.find('ListID').text
        self.data_extension_value = self.xml.find('ListID').text

    def parse_account_xml(self):
        self.id = self.xml.find('ListID').text
        self.time_created = self.xml.find('TimeCreated').text
        self.time_last_modified = self.xml.find('TimeModified').text
        self.edit_sequence = self.xml.find('EditSequence').text
        self.name = self.xml.find('Name').text
        self.full_name = self.xml.find('FullName').text
        self.is_active = self.xml.find('IsActive').text
        self.sublevel = self.xml.find('Sublevel').text if not [] else None
        self.account_type = self.xml.find('AccountType').text
        self.special_account_type = self.xml.find('SpecialAccountType').text
        self.account_number = self.xml.find('AccountNumber').text
        self.bank_number = self.xml.find('BankNumber').text
        self.desc = self.xml.find('Desc').text
        self.balance = self.xml.find('Balance').text
        self.total_balance = self.xml.find('TotalBalance').text
        self.cash_flow_classification = self.xml.find('CashFlowClassification').text




class Accounts():
    def __init__(self):
        pass

    def add_list_to_xml(self, root, item_list, element_name):
        for list_item in item_list:
            xml = et.Element(element_name).text = list_item
            root.insert(xml)
        return root

    def add_element_to_xml(self, root, element, element_name):
        et.SubElement(root, element_name).text = element
        return root

    def add_account_type_to_xml(self, root, account_type):
        account_types = ["AccountsPayable", "AccountsReceivable", "Bank", "CostOfGoodsSold", "CreditCard", "Equity",
                         "Expense", "FixedAsset", "Income", "LongTermLiability", "NonPosting", "OtherAsset",
                         "OtherCurrentAsset", "OtherCurrentLiability", "OtherExpense", "OtherIncome"]
        if account_type in account_types:
            xml = et.Element('AccountType').text = account_type
            root.insert(xml)
        else:
            raise Exception(f'''
                                The account_type given ("{account_type}") is not in the approved list of account types \n
                                Please choose an account type from the following: \n
                                "AccountsPayable", "AccountsReceivable", "Bank", "CostOfGoodsSold", "CreditCard", \n
                                "Equity", "Expense", "FixedAsset", "Income", "LongTermLiability", "NonPosting", \n
                                "OtherAsset", "OtherCurrentAsset", "OtherCurrentLiability", "OtherExpense", "OtherIncome"
                                ''')
        return root

    def response_to_df(self, response):
        tree = et.fromstring(response)
        accounts_xml = tree.xpath('/QBXML/QBXMLMsgsRs/AccountQueryRs/AccountRet')
        accounts = {}
        for account_xml in accounts_xml:
            account = Account(account_xml)
            account.parse_account_xml()
            accounts[account.name] = account

        xml2df = XML2DataFrame(et.tostring(tree))
        xml_df = xml2df.process_data()
        print(response)

    def quick_search(self,
                     list_id_list=[],
                     full_name_list=[],
                     max_return=None,
                     active_status='All',
                     from_modified_date=None,
                     to_modified_date=None,
                     account_type=None
                     ):
        """
        :param list_id_list: A list strings that represent the backend ID (not UI or Report facing ID).
        :param full_name_list: A list of strings with the accounts full_name.  Must be exact.
        :param max_return: An Int that represents the maximun quantity returned with the response.
        :param active_status: A string that may have on of the following values: ActiveOnly, InactiveOnly, All
        :param from_modified_date: A Python date.datetime object or a date string.
        :param to_modified_date: A Python date.datetime object or a date string.
        :param account_type: A string that may have one of the following values: AccountsPayable, AccountsReceivable,
                                Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income,
                                LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability,
                                OtherExpense, OtherIncome
        :param currency_id: A string that represent the backend ID (not UI or Report facing ID).
        :param currency_full_name: A string that represents the name of exact currency full_name.
        :param limit_return_fields_to: A list of strings that represent the attributes (columns/fields) that you want to
                                            limit the returning data to.  Typically it's used if you have a large company
                                            file and you want to improve performance.
        :return: A pandas dataframe of the accounts
        """
        root = et.Element('AccountQueryRq')
        if not list_id_list:
            root = self.add_list_to_xml(root, list_id_list, 'ListID')
        if not full_name_list:
            root = self.add_list_to_xml(root, full_name_list, 'FullName')
        if max_return is not None:
            root = self.add_element_to_xml(root, max_return, 'MaxReturn')
        if active_status is not None:
            root = self.add_element_to_xml(root, active_status, 'ActiveStatus')
        if from_modified_date is not None:
            root = self.add_element_to_xml(root, from_modified_date, 'FromModifiedDate')
        if to_modified_date is not None:
            root = self.add_element_to_xml(root, to_modified_date, 'ToModifiedDate')
        if account_type is not None:
            root = self.add_account_type_to_xml(root, account_type)
        qb = SessionManager()
        response = qb.send_xml(root)
        df = self.response_to_df(response)
        # todo: limit_return_fields_to = []

