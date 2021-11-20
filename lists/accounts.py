from lxml import etree as et

class Accounts():
    def __init__(self):
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

    def add_list_to_xml(self, root, item_list, element_name):
        for list_item in item_list:
            xml = et.Element(element_name).text = list_item
            root.insert(xml)
        return root

    def add_element_to_xml(self, root, element, element_name):
        xml = et.Element(element_name).text = element
        root.insert(xml)
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

    def quick_search(self,
                     list_id_list=[],
                     full_name_list=[],
                     max_return=None,
                     active_status='ActiveOnly',
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

        # todo: limit_return_fields_to = []