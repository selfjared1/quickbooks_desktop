from core.base import QBListBase

from typing import Optional
import attr
from core.special_fields import Ref
from core.base import QBListBase

@attr.s(auto_attribs=True)
class Account(QBListBase):
    Sublevel: Optional[int] = None
    AccountType: Optional[str] = None
    SpecialAccountType: Optional[str] = None
    AccountNumber: Optional[str] = None
    BankNumber: Optional[str] = None
    Balance: Optional[float] = None
    TotalBalance: Optional[float] = None
    TaxLineRetInfoRet_TaxLineID: Optional[int] = None
    TaxLineRetInfoRet_TaxLineName: Optional[str] = None
    CashFlowClassification: Optional[str] = None
    CurrencyRef_ListID: Optional[str] = None
    CurrencyRef_ListFullName: Optional[str] = None
    ParentRef: Optional[Ref] = None