from pydantic import BaseModel, validator, PrivateAttr
from typing import Any
from pydantic.utils import GetterDict
from xml.etree.ElementTree import fromstring
from datetime import datetime
from utility import snake_to_camel_str, camel_to_snake_str

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

class AccountGetter(GetterDict):
    def get(self, key: str, default: Any) -> Any:
        key = camel_to_snake_str(key)
        if key in {'ParentRef', 'BankNumber', 'TaxLineInfoRet', 'CurrencyRef'}:
            return self._obj.attrib.get(key, default)
        else:
            return self._obj.find(key).text

class Account(BaseModel):
    list_id: str = None
    time_created: datetime = None
    time_modified: datetime = None
    _synced_at: datetime = PrivateAttr(default_factory=datetime.now)
    edit_sequence: int = None
    name: str = None
    full_name: str = None
    is_active: bool = None
    parent_ref: Account = None
    parent_ref_list_id: str = None
    parent_ref_full_name: str = None
    sublevel: int = None
    account_type: str = None
    special_account_type: str = None
    account_number: str = None
    bank_number: str = None
    desc: str = None
    balance: float = None
    total_balance: float = None
    tax_line_info_ret_tax_line_id: str = None
    tax_line_info_ret_tax_line_name: str = None
    cash_flow_classification: str = None
    currency_ref_list_id: str = None
    currency_ref_full_name: str = None

    class Config:
        orm_mode = True
        getter_dict = AccountGetter

    @validator('SpecialAccountType')
    def validate_special_account_type(cls, value):
        if value not in ALLOWED_SPECIAL_ACCOUNT_TYPES:
            raise ValueError(f"{value} is not a valid special account type")
        return value

    @validator('AccountType')
    def validate_account_type(cls, value):
        if value not in ALLOWED_ACCOUNT_TYPES:
            raise ValueError(f"{value} is not a valid account type")
        return value

    @validator('CashFlowClassification')
    def validate_cash_flow_classification(cls, value):
        if value not in ALLOWED_CASH_FLOW_CLASSIFICATION:
            raise ValueError(f"{value} is not a valid cash flow classification type")
        return value

    @validator('AccountNumber')
    def validate_account_number(cls, value):
        if len(value) > 6:
            raise ValueError("Account number cannot be longer than 6 characters")
        return value

if __name__ == '__main__':
    xml_str = """
    <AccountRet>
        <ListID>790001-1048186768</ListID>
        <TimeCreated>2003-03-20T12:59:28-07:00</TimeCreated>
        <TimeModified>2025-12-15T09:56:41-07:00</TimeModified>
        <EditSequence>1765817801</EditSequence>
        <Name>Sales Orders</Name>
        <FullName>Sales Orders</FullName>
        <IsActive>true</IsActive>
        <Sublevel>0</Sublevel>
        <AccountType>NonPosting</AccountType>
        <SpecialAccountType>SalesOrders</SpecialAccountType>
        <AccountNumber>5</AccountNumber>
        <Balance>0.00</Balance>
        <TotalBalance>0.00</TotalBalance>
        <CashFlowClassification>NotApplicable</CashFlowClassification>
    </AccountRet>
    """

    account = Account.from_orm(fromstring(xml_str))
    print(account)