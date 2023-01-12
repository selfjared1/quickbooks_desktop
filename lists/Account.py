from datetime import datetime
from typing import List
from attrs import define
from utility.utilities import from_lxml_elements
import pandas as pd

@define
class Account:
    ListID: str = None
    TimeCreated: datetime = None
    TimeModified: datetime = None
    EditSequence: str = None
    Name: str = None
    FullName: str = None
    IsActive: bool = None
    ParentRef: dict = None
    Sublevel: int = None
    AccountType: str = None
    SpecialAccountType: str = None
    AccountNumber: str = None
    BankNumber: str = None
    Desc: str = None
    Balance: float = None
    TotalBalance: float = None
    TaxLineInfoRetTaxLineID: str = None
    TaxLineInfoRetTaxLineName: str = None
    CashFlowClassification: str = None
    CurrencyRefListID: str = None
    CurrencyRefFullName: str = None
    DataExtRet: list = None

    @classmethod
    def from_xml(cls, elements):
        account = from_lxml_elements(cls, elements, combine_with_child_list=['TaxLineInfoRet', 'CurrencyRef'])
        return account
