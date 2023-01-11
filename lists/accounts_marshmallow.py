import xmltodict
from marshmallow import Schema, fields
from utility import snake_to_camel_str, camel_to_snake_dict

ALLOWED_ACCOUNT_TYPES = [
    'AccountsPayable', 'AccountsReceivable', 'Bank', 'CostOfGoodsSold',
    'CreditCard', 'Equity', 'Expense', 'FixedAsset', 'Income',
    'LongTermLiability', 'NonPosting', 'OtherAsset', 'OtherCurrentAsset',
    'OtherCurrentLiability', 'OtherExpense', 'OtherIncome'
]

ALLOWED_SPECIAL_ACCOUNT_TYPES = [
    'AccountsPayable', 'AccountsReceivable', 'CondenseItemAdjustmentExpenses',
    'CostOfGoodsSold', 'DirectDepositLiabilities', 'Estimates', 'ExchangeGainLoss',
    'InventoryAssets', 'ItemReceiptAccount', 'OpeningBalanceEquity',
    'PayrollExpenses', 'PayrollLiabilities', 'PettyCash', 'PurchaseOrders',
    'ReconciliationDifferences', 'RetainedEarnings', 'SalesOrders',
    'SalesTaxPayable', 'UncategorizedExpenses', 'UncategorizedIncome',
    'UndepositedFunds'
]

ALLOWED_CASH_FLOW_CLASSIFICATION = ['None', 'Operating', 'Investing', 'Financing', 'NotApplicable']

def validate_account_type(value):
    if value not in ALLOWED_ACCOUNT_TYPES:
        raise ValueError('Invalid account type.  Valid types include: ' + str(ALLOWED_ACCOUNT_TYPES))
    return value

def validate_special_account_type(value):
    if value not in ALLOWED_SPECIAL_ACCOUNT_TYPES:
        raise ValueError('Invalid account type.  Valid types include: ' + str(ALLOWED_SPECIAL_ACCOUNT_TYPES))
    return value

def validate_account_number(value):
    if len(value) > 6:
        raise ValueError('Account number must be 6 digits or less')
    return value

def validate_cash_flow_classification(value):
    if value not in ALLOWED_CASH_FLOW_CLASSIFICATION:
        raise ValueError('Invalid cash flow classification.  Valid types include: ' + str(ALLOWED_CASH_FLOW_CLASSIFICATION))
    return value

class Account(Schema):
    def __init__(self):
        self._list_id = fields.String()
        self._time_created = fields.DateTime()
        self._time_modified = fields.DateTime()
        self._edit_sequence = fields.Integer()
        self.name = fields.String()
        self._full_name = fields.String() #todo: Allow full name auto create parent association
        self.is_active = fields.Boolean()
        self.parent_ref_list_id = fields.String()
        self._parent_ref_full_name = fields.String()
        self.sublevel = fields.Integer() #todo: validate int length
        self.account_type = fields.String(validate=validate_account_type)
        self.special_account_type = fields.String(validate=validate_special_account_type)
        self.account_number = fields.String(validate=validate_account_number)
        self.bank_number = fields.String() #todo: validate string length
        self.desc = fields.String() #todo: validate string length
        self._balance = fields.Decimal(as_string=True)
        self._total_balance = fields.Decimal(as_string=True)
        self.tax_line_info_ret_tax_line_id = fields.String() #todo: validate
        self.tax_line_info_ret_tax_line_name = fields.String() #todo: validate
        self.cash_flow_classification = fields.String(validate=validate_cash_flow_classification)
        self.currency_ref_list_id = fields.String() #todo: validate
        self.currency_ref_full_name = fields.String() #todo: validate
        #todo: self.data_ext_ret = None

    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in self.items())
        return f'AccountSchema({attrs})'

    @property
    def list_id(self):
        return self._list_id

    def _set_list_id(self, value):
        setattr(self, '_list_id', value)

    @property
    def time_created(self):
        return self._time_created

    def _set_time_created(self, value):
        setattr(self, '_time_created', value)

    @property
    def time_modified(self):
        return self._time_modified

    def _set_time_modified(self, value):
        setattr(self, '_time_modified', value)

    @property
    def edit_sequence(self):
        return self._edit_sequence

    def _set_edit_sequence(self, value):
        setattr(self, '_edit_sequence', value)

    @property
    def full_name(self):
        return self._full_name

    def _set_full_name(self, value):
        setattr(self, '_full_name', value)

    @property
    def parent_ref_full_name(self):
        return self._full_name

    def _set_parent_ref_full_name(self, value):
        setattr(self, '_parent_ref_full_name', value)

    def _set_parent_ref(self, value):
        self._set_parent_ref_full_name(value['full_name'])
        setattr(self, 'parent_ref_list_id', value['list_id'])

    @property
    def balance(self):
        return self._balance

    def _set_balance(self, value):
        setattr(self, '_balance', value)

    @property
    def total_balance(self):
        return self.total_balance

    def _set_total_balance(self, value):
        setattr(self, '_total_balance', value)

    @property
    def tax_line_info_ret(self):
        return self._tax_line_info_ret_tax_line_name

    def _set_tax_line_info_ret(self, value):
        setattr(self, '_tax_line_info_ret', value)
    
    @classmethod
    def from_xml(cls, xml_string):
        key_requires_setter = ['list_id', 'time_created', 'time_modified', 'edit_sequence', 'full_name',
                               'balance', 'total_balance', 'parent_ref', 'tax_line_info_ret', 'currency_ref']
        data = xmltodict.parse(xml_string)['AccountRet']
        data = camel_to_snake_dict(data)
        account = cls()
        for k, v in data.items():
            if k in key_requires_setter:
                setter = getattr(account, '_set_' + k)
                setter(v)
            else:
                setattr(account, k, v)
        return account

        # account.list_id = account._set_list_id(data.get('ListID'))
        # account.time_created = account._set_time_created(data.get('TimeCreated'))
        # account.time_modified = account._set_time_modified(data.get('TimeModified'))
        # account.edit_sequence = account._set_edit_sequence(data.get('EditSequence'))
        # account.name = data.get('Name')
        # account.full_name = account._set_full_name(data.get('FullName'))
        # account.is_active = data.get('IsActive')
        # account.parent_ref = data.get('ParentRef')
        # account.parent_ref_list_id = data.get('ParentRef', {}).get('ListID')
        # account.parent_ref_full_name = account._set_parent_ref_full_name(data.get('ParentRef', {}).get('FullName'))
        # account.sublevel = data.get('Sublevel')
        # account.account_type = data.get('AccountType')
        # account.special_account_type = data.get('SpecialAccountType')
        # account.account_number = data.get('AccountNumber')
        # account.bank_number = data.get('BankNumber')
        # account.desc = data.get('Desc')
        # account.balance = data.get('Balance')
        # account.total_balance = data.get('TotalBalance')
        # account.tax_line_info_ret_tax_line_id = data.get('TaxLineInfoRet', {}).get('TaxLineID')
        # account.tax_line_info_ret_tax_line_name = data.get('TaxLineInfoRet', {}).get('TaxLineName')
        # account.cash_flow_classification = data.get('CashFlowClassification')
        # account.currency_ref_list_id = data.get('CurrencyRef', {}).get('ListID')
        # account.currency_ref_full_name = data.get('CurrencyRef', {}).get('FullName')
        # # todo: account.data_ext_ret = data.get('DataExtRet')

class Accounts(Schema):
    def __init__(self):
        self.account = fields.Nested(Account, many=True)

