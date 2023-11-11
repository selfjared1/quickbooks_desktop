from core.base import QBListBase

from typing import Optional
import attr
from core.special_fields import Ref, DataExtRet
from core.base import QBListBase


def account_type_validator(instance, attribute, value):
    allowed_types = [
        "AccountsPayable", "AccountsReceivable", "Bank", "CostOfGoodsSold",
        "CreditCard", "Equity", "Expense", "FixedAsset", "Income",
        "LongTermLiability", "NonPosting", "OtherAsset", "OtherCurrentAsset",
        "OtherCurrentLiability", "OtherExpense", "OtherIncome"
    ]
    if value not in allowed_types:
        raise ValueError(f"{value} is not a valid account type.  Allowed types are: {allowed_types}")

def special_account_type_validator(instance, attribute, value):
    allowed_special_account_types = [
        "AccountsPayable", "AccountsReceivable", "CondenseItemAdjustmentExpenses",
        "CostOfGoodsSold", "DirectDepositLiabilities", "Estimates", "ExchangeGainLoss",
        "InventoryAssets", "ItemReceiptAccount", "OpeningBalanceEquity",
        "PayrollExpenses", "PayrollLiabilities", "PettyCash", "PurchaseOrders",
        "ReconciliationDifferences", "RetainedEarnings", "SalesOrders",
        "SalesTaxPayable", "UncategorizedExpenses", "UncategorizedIncome",
        "UndepositedFunds"
    ]
    if value not in allowed_special_account_types:
        raise ValueError(f"{value} is not a valid special account type.  Allowed types are: {allowed_special_account_types}")

def cash_flow_classification_validator(instance, attribute, value):
    allowed_values = ["None", "Operating", "Investing", "Financing", "NotApplicable"]
    if value not in allowed_values:
        raise ValueError(f"{value} is not a valid cash flow classification")

@attr.s(auto_attribs=True)
class Account(QBListBase):

    Name: Optional[str] = None
    FullName: Optional[str] = None
    IsActive: Optional[bool] = None
    ParentRef: Optional[Ref] = None
    Sublevel: Optional[int] = None
    AccountType: Optional[str] = attr.ib(default=None, validator=account_type_validator)
    SpecialAccountType: Optional[str] = attr.ib(default=None, validator=special_account_type_validator)
    AccountNumber: Optional[str] = None
    BankNumber: Optional[str] = None
    Balance: Optional[float] = None
    TotalBalance: Optional[float] = None
    TaxLineRetInfoRet_TaxLineID: Optional[int] = None
    TaxLineRetInfoRet_TaxLineName: Optional[str] = None
    CashFlowClassification: Optional[str] = attr.ib(default=None, validator=cash_flow_classification_validator)
    CurrencyRef: Optional[Ref] = None
    DataExtRet: Optional[DataExtRet] = None

    def to_ref(self, ref_label=None):
        if not ref_label:
            ref_label = str(self.__class__.__name__) + "Ref"
        elif ref_label[-3:] == "Ref":
            pass
        else:
            ref_label = ref_label + "Ref"

        ref = Ref(
            ref_label=ref_label,
            id_name="ListID",
            ID=self.ListID,
            name_name="FullName",
            Name=self.FullName
        )
        return ref

