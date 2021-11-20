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

    def search(self,
               list_id_list=[],
               max_returned=None,
               active_status='ActiveOnly',
               from_modified_date=None,
               to_modified_date=None,
               name_starts_with=None,
               name_contains=None,
               name_ends_with=None,
               name_range=('',''),
               account_type=None,
               currency_id=None,
               currency_full_name=None,
               limit_return_fields_to=[],
               owner_id_list=[]
               ):
        """
        :param list_id: A list strings that represent the backend ID (not UI or Report facing ID).
        :param max_returned: An Int that represents the maximun quantity returned with the response.
        :param active_status: A string that may have on of the following values: ActiveOnly, InactiveOnly, All
        :param from_modified_date: A Python date.datetime object or a date string.
        :param to_modified_date: A Python date.datetime object or a date string.
        :param name_starts_with:  A string that the account Full Name would start with. Cannot Be combined with
                                    name_contains, or name_ends_with.
        :param name_contains:  A string that the account Full Name would have in it. Cannot Be combined with
                                    name_starts_with, or name_ends_with.
        :param name_ends_with:  A string that the account Full Name would end with. Cannot Be combined with
                                    name_starts_with, or name_contains.
        :param name_range:  A string that the account Full Name would end with.
        :param account_type: A string that may have one of the following values: AccountsPayable, AccountsReceivable,
                                Bank, CostOfGoodsSold, CreditCard, Equity, Expense, FixedAsset, Income,
                                LongTermLiability, NonPosting, OtherAsset, OtherCurrentAsset, OtherCurrentLiability,
                                OtherExpense, OtherIncome
        :param currency_id: A string that represent the backend ID (not UI or Report facing ID).
        :param currency_full_name: A string that represents the name of exact currency full_name.
        :param limit_return_fields_to: A list of strings that represent the attributes (columns/fields) that you want to
                                            limit the returning data to.  Typically it's used if you have a large company
                                            file and you want to improve performance.
        :param owner_id_list: A list of strings representing the custom data owner id's.  This is very rarely used.
        :return: A pandas dataframe of the accounts
        """
        # for key, value in kwargs.items():
        #     if hasattr(self, key):
        #         self.__setattr__(key, value)
        #     else:
        #         raise Exception(f'The key "{key}" does not match the available attributes for accounts')
        root = et.Element('AccountQueryRq')
        if not list_id_list:
            for list_id in list_id_list:
                id_xml = et.Element('ListID').text = list_id
                root.insert()
        if self.full_name is not None:
            et.SubElement(root, 'FullName')
        if self.
