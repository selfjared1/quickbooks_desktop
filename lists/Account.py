from core.base import QBListBase

from typing import Optional
import attr
from core.special_fields import Ref, DataExtRet, QBDate
from core.base import QBListBase


def account_type_validator(instance, attribute, value):
    if value is None:
        return
    else:
        allowed_types = [
            "AccountsPayable", "AccountsReceivable", "Bank", "CostOfGoodsSold",
            "CreditCard", "Equity", "Expense", "FixedAsset", "Income",
            "LongTermLiability", "NonPosting", "OtherAsset", "OtherCurrentAsset",
            "OtherCurrentLiability", "OtherExpense", "OtherIncome"
        ]
        if value not in allowed_types:
            raise ValueError(f"{value} is not a valid account type.  Allowed types are: {allowed_types}")
        else:
            return

def special_account_type_validator(instance, attribute, value):
    if value is None:
        return
    else:
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
        else:
            return

def cash_flow_classification_validator(instance, attribute, value):
    if value is None:
        return
    else:
        allowed_values = ["None", "Operating", "Investing", "Financing", "NotApplicable"]
        if value not in allowed_values:
            raise ValueError(f"{value} is not a valid cash flow classification")
        else:
            return

@attr.s(auto_attribs=True)
class Account(QBListBase):
    class_dict = {
        **QBListBase.class_dict,
        "CurrencyRef": Ref,
        "ParentRef": Ref,
        "DataExtRet": DataExtRet
    }

    Name: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': True, 'Mod': False, 'Query': None}})
    FullName: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': False}})
    IsActive: Optional[bool] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    ParentRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    Sublevel: Optional[int] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    AccountType: Optional[str] = attr.ib(default=None, validator=account_type_validator, metadata={'is_required': {'Add': True, 'Mod': False, 'Query': None}})
    SpecialAccountType: Optional[str] = attr.ib(default=None, validator=special_account_type_validator, metadata={'is_required': {'Add':False, 'Mod': False, 'Query': None}})
    AccountNumber: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    BankNumber: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    Balance: Optional[float] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    TotalBalance: Optional[float] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    TaxLineRetInfoRet_TaxLineID: Optional[int] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    TaxLineRetInfoRet_TaxLineName: Optional[str] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    CashFlowClassification: Optional[str] = attr.ib(default=None, validator=cash_flow_classification_validator, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    CurrencyRef: Optional[Ref] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})
    DataExtRet: Optional[DataExtRet] = attr.ib(default=None, metadata={'is_required': {'Add': False, 'Mod': False, 'Query': None}})

    def to_ref(self, name_of_start_tag=None):
        if not name_of_start_tag:
            name_of_start_tag = str(self.__class__.__name__) + "Ref"
        elif name_of_start_tag[-3:] == "Ref":
            pass
        else:
            name_of_start_tag = name_of_start_tag + "Ref"

        ref = Ref(
            ref_label=name_of_start_tag,
            id_name="ListID",
            ID=self.ListID,
            name_name="FullName",
            Name=self.FullName
        )
        return ref

